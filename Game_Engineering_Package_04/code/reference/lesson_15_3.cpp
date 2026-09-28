// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "language.hpp"
#include <string>
#include <utility>
#include <vector>


int main() {
    return p4test::run("15.3", [] {

        using namespace ge::lang;
        const auto code=compile(parse("8-3*2"));CHECK(code.size()==5);CHECK(run(code,5)==2);
        CHECK(p4test::throws<Error>([&]{run(code,4);}));
        CHECK(p4test::throws<Error>([]{run(Program{{Op::Add,0,0}});}));
        CHECK(p4test::throws<Error>([]{run(Program{{static_cast<Op>(255),0,0}});}));
        CHECK(p4test::throws<Error>([]{run(Program{{Op::Push,1,0},{Op::Push,2,0}});}));
        CHECK(p4test::throws<Error>([]{run(Program{});}));
        CHECK(p4test::throws<Error>([]{run(Program{{Op::Push,value_limit+1,0}});}));
        CHECK(p4test::throws<Error>([]{run(Program{{Op::Neg,0,0}});}));
        Limits l;l.stack=1;CHECK(p4test::throws<Error>([&]{run(code,100,l);}));
        l=Limits{};l.instructions=4;CHECK(p4test::throws<Error>([&]{run(code,100,l);}));
        CHECK(p4test::throws<Error>([&]{run(code,0);}));
        for(int a=-9;a<=9;++a)for(int b=1;b<=9;++b) {
            const auto text="("+std::to_string(a)+"-"+std::to_string(b)+")/3";
            const auto tree=parse(text);CHECK(run(compile(tree))==evaluate(tree));CHECK(run(compile(tree))==(a-b)/3);
        }
        const auto failing=parse("1/(2-2)");std::pair<std::size_t,std::string> tree_error;
        try {evaluate(failing);CHECK(false);}catch(const Error& e){tree_error={e.pos,e.category};}
        try {run(compile(failing));CHECK(false);}catch(const Error& e){CHECK(tree_error==std::pair{e.pos,e.category});}

    });
}
