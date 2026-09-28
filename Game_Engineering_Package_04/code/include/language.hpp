#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace ge::lang {
using Value=std::int64_t;
inline constexpr Value value_limit=1000000000;
struct Limits {
    std::size_t source=16384,tokens=4096,nodes=4096,depth=64;
    std::size_t instructions=4096,stack=256;
};
struct Error:std::runtime_error {
    std::size_t pos;
    std::string category;
    Error(std::size_t p,std::string message)
      :std::runtime_error(message+" at byte "+std::to_string(p)),
       pos(p),category(std::move(message)) {}
};
inline Value checked(Value v,std::size_t pos) {
    if(v < -value_limit || v > value_limit) throw Error(pos,"numeric range");
    return v;
}
enum class Op:unsigned { Push,Add,Sub,Mul,Div,Neg };
inline Value apply(Op op,Value left,Value right,std::size_t pos) {
    // The operands are always range-checked before using 64-bit intermediates.
    checked(left,pos);checked(right,pos);
    switch(op) {
    case Op::Add:return checked(left+right,pos);
    case Op::Sub:return checked(left-right,pos);
    case Op::Mul:return checked(left*right,pos); // <= 10^18 before checking
    case Op::Div:
        if(right==0) throw Error(pos,"division by zero");
        return checked(left/right,pos); // truncates toward zero
    case Op::Neg:return checked(-left,pos);
    default:throw Error(pos,"invalid arithmetic opcode");
    }
}
enum class Kind { Number,Plus,Minus,Star,Slash,LParen,RParen,End };
struct Token { Kind kind;Value value;std::size_t pos; };
inline bool digit(char c) { return c>='0' && c<='9'; }
inline bool whitespace(char c) {
    return c==' ' || c=='\t' || c=='\n' || c=='\r' || c=='\f' || c=='\v';
}
inline std::vector<Token> lex(std::string_view source,const Limits& limits={}) {
    if(source.size()>limits.source) throw Error(limits.source,"source budget");
    std::vector<Token> tokens;
    auto emit=[&](Token token) {
        if(tokens.size()>=limits.tokens) throw Error(token.pos,"token budget");
        tokens.push_back(token);
    };
    for(std::size_t i=0;i<source.size();) {
        const char c=source[i];
        if(whitespace(c)) { ++i;continue; }
        const auto pos=i;
        if(digit(c)) {
            Value value=0;
            while(i<source.size() && digit(source[i])) {
                const Value d=source[i]-'0';
                if(value>(value_limit-d)/10) throw Error(pos,"numeric range");
                value=value*10+d;++i;
            }
            emit({Kind::Number,value,pos});continue;
        }
        Kind kind;
        switch(c) {
        case '+':kind=Kind::Plus;break;case '-':kind=Kind::Minus;break;
        case '*':kind=Kind::Star;break;case '/':kind=Kind::Slash;break;
        case '(':kind=Kind::LParen;break;case ')':kind=Kind::RParen;break;
        default:throw Error(pos,"unknown name or invalid token");
        }
        ++i;emit({kind,0,pos});
    }
    // End counts toward the token limit, by specification.
    emit({Kind::End,0,source.size()});return tokens;
}
struct Node {
    Op op=Op::Push;Value value=0;
    std::size_t left=0,right=0,pos=0,depth=1;
};
struct Tree { std::vector<Node> nodes;std::size_t root=0; };
class Parser {
    std::vector<Token> tokens_;
    std::size_t cursor_=0;
    Tree tree_;
    Limits limits_;
    const Token& peek() const { return tokens_.at(cursor_); }
    Token consume() { return tokens_.at(cursor_++); }
    std::size_t node(Node n) {
        if(tree_.nodes.size()>=limits_.nodes) throw Error(n.pos,"node budget");
        if(n.depth>limits_.depth) throw Error(n.pos,"AST depth budget");
        tree_.nodes.push_back(n);return tree_.nodes.size()-1;
    }
    std::size_t expression(std::size_t nesting) {
        auto left=term(nesting);
        while(peek().kind==Kind::Plus || peek().kind==Kind::Minus) {
            const auto token=consume();const auto right=term(nesting);
            const auto depth=1+std::max(tree_.nodes[left].depth,tree_.nodes[right].depth);
            left=node({token.kind==Kind::Plus?Op::Add:Op::Sub,0,left,right,token.pos,depth});
        }
        return left;
    }
    std::size_t term(std::size_t nesting) {
        auto left=primary(nesting);
        while(peek().kind==Kind::Star || peek().kind==Kind::Slash) {
            const auto token=consume();const auto right=primary(nesting);
            const auto depth=1+std::max(tree_.nodes[left].depth,tree_.nodes[right].depth);
            left=node({token.kind==Kind::Star?Op::Mul:Op::Div,0,left,right,token.pos,depth});
        }
        return left;
    }
    std::size_t primary(std::size_t nesting) {
        if(nesting>limits_.depth) throw Error(peek().pos,"nesting budget");
        const auto token=consume();
        if(token.kind==Kind::Number) return node({Op::Push,token.value,0,0,token.pos,1});
        if(token.kind==Kind::Minus) {
            const auto child=primary(nesting+1);
            return node({Op::Neg,0,child,0,token.pos,1+tree_.nodes[child].depth});
        }
        if(token.kind==Kind::LParen) {
            const auto root=expression(nesting+1);
            if(peek().kind!=Kind::RParen) throw Error(peek().pos,"expected closing parenthesis");
            consume();return root;
        }
        throw Error(token.pos,"expected number or parenthesis");
    }
public:
    Parser(std::string_view source,Limits limits={})
        :tokens_(lex(source,limits)),limits_(limits) {
        // Hard ceilings keep recursion bounded even if a caller edits limits.
        if(limits_.depth>64) throw std::invalid_argument("depth cannot exceed 64");
    }
    Tree parse() {
        tree_.root=expression(0);
        if(peek().kind!=Kind::End) throw Error(peek().pos,"trailing token");
        return std::move(tree_);
    }
};
inline Tree parse(std::string_view source,Limits limits={}) {
    return Parser(source,limits).parse();
}
// Tree evaluation/compilation require a parser-produced arena, not raw,
// externally editable AST records. Untrusted input enters through parse/VM.
inline Value evaluate_node(const Tree& tree,std::size_t index) {
    const auto& n=tree.nodes.at(index);
    if(n.op==Op::Push) return checked(n.value,n.pos);
    const auto left=evaluate_node(tree,n.left);
    if(n.op==Op::Neg) return apply(n.op,left,0,n.pos);
    const auto right=evaluate_node(tree,n.right);
    return apply(n.op,left,right,n.pos);
}
inline Value evaluate(const Tree& tree) { return evaluate_node(tree,tree.root); }
struct Instruction { Op op;Value value=0;std::size_t pos=0; };
using Program=std::vector<Instruction>;
inline void emit_node(const Tree& tree,std::size_t index,Program& output,
                      const Limits& limits) {
    const auto& n=tree.nodes.at(index);
    if(n.op!=Op::Push) {
        emit_node(tree,n.left,output,limits);
        if(n.op!=Op::Neg) emit_node(tree,n.right,output,limits);
    }
    if(output.size()>=limits.instructions) throw Error(n.pos,"instruction budget");
    output.push_back({n.op,n.value,n.pos});
}
inline Program compile(const Tree& tree,Limits limits={}) {
    Program output;emit_node(tree,tree.root,output,limits);return output;
}
inline Value run(const Program& code,std::size_t fuel=4096,Limits limits={}) {
    if(code.size()>limits.instructions) throw Error(0,"instruction budget");
    std::vector<Value> stack;
    for(const auto& ins:code) {
        if(fuel==0) throw Error(ins.pos,"execution budget");
        --fuel;
        switch(ins.op) {
        case Op::Push:
            if(stack.size()>=limits.stack) throw Error(ins.pos,"stack budget");
            stack.push_back(checked(ins.value,ins.pos));break;
        case Op::Neg:
            if(stack.empty()) throw Error(ins.pos,"stack underflow");
            stack.back()=apply(Op::Neg,stack.back(),0,ins.pos);break;
        case Op::Add:case Op::Sub:case Op::Mul:case Op::Div: {
            if(stack.size()<2) throw Error(ins.pos,"stack underflow");
            const auto right=stack.back();stack.pop_back();
            const auto left=stack.back();stack.pop_back();
            stack.push_back(apply(ins.op,left,right,ins.pos));break;
        }
        default:throw Error(ins.pos,"invalid opcode");
        }
    }
    if(stack.size()!=1) throw Error(code.empty()?0:code.back().pos,"final stack shape");
    return stack.back();
}
inline Tree fold(Tree tree) {
    // Parser appends children before parents. Iterate bottom-up without
    // retaining references across vector mutation (no nodes appended here).
    for(auto& n:tree.nodes) {
        if(n.op==Op::Push) continue;
        const Node left=tree.nodes.at(n.left);
        if(left.op!=Op::Push) continue;
        if(n.op==Op::Neg) {
            n.value=apply(Op::Neg,left.value,0,n.pos);n.op=Op::Push;n.depth=1;
            continue;
        }
        const Node right=tree.nodes.at(n.right);
        if(right.op!=Op::Push) continue;
        try {
            const auto result=apply(n.op,left.value,right.value,n.pos);
            n.value=result;n.op=Op::Push;n.depth=1;
        } catch(const Error&) {
            // Keep the failing operator for the same runtime diagnostic.
        }
    }
    return tree;
}
inline bool decimal_fsm(std::string_view text) {
    enum class State {Start,Digits,Dead};State state=State::Start;
    for(const char c:text) {
        if(state==State::Dead) continue;
        state=digit(c)?State::Digits:State::Dead;
    }
    return state==State::Digits;
}
}
