// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "language.hpp"
#include <string>
#include <utility>


template<class Function>std::pair<std::size_t,std::string> capture_error(Function f) {
    try{f();}catch(const ge::lang::Error& e){return {e.pos,e.category};}
    throw std::runtime_error("expected language failure");
}

int main() {
    return p4test::run("15.4", [] {

        using namespace ge::lang;
        CHECK(!decimal_fsm(""));CHECK(decimal_fsm("007"));CHECK(!decimal_fsm("7x"));CHECK(!decimal_fsm(" 7"));
        CHECK(decimal_fsm("99999999999999999999"));
        CHECK(p4test::throws<Error>([]{parse("99999999999999999999");}));
        auto tree=parse("2+3*4");const auto folded=fold(tree);
        CHECK(evaluate(folded)==14);CHECK(run(compile(folded))==14);CHECK(compile(folded).size()==1);
        for(const auto* text:{"(1/0)*0","1000000000+1","(1/0)+(1000000000+1)"}) {
            const auto original=parse(text);const auto optimized=fold(original);
            const auto a=capture_error([&]{return evaluate(original);});
            const auto b=capture_error([&]{return run(compile(optimized));});CHECK(a==b);
        }
        for(int a=-10;a<=10;++a)for(int b=-10;b<=10;++b) {
            auto input=parse("("+std::to_string(a)+"+"+std::to_string(b)+")*2");
            const auto optimized=fold(input);CHECK(evaluate(input)==(a+b)*2);
            CHECK(run(compile(input))==run(compile(optimized)));CHECK(evaluate(optimized)==(a+b)*2);
        }

    });
}
