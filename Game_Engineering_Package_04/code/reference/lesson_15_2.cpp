// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "language.hpp"
#include <string>
#include <utility>
#include <vector>


int main() {
    return p4test::run("15.2", [] {

        using namespace ge::lang;
        const std::vector<std::pair<std::string,Value>> golden{
            {"2+3*4",14},{"(2+3)*4",20},{"8-3-1",4},{"-8/3",-2},
            {"--3",3},{" 007 \n",7},{"1000000000",1000000000},{"0",0}};
        for(const auto& [text,value]:golden)CHECK(evaluate(parse(text))==value);
        for(const auto* bad:{"","2 3","speed+1","(2+3","2+","1/(2-2)","1000000001","1000000000+1"})
            CHECK(p4test::throws<Error>([&]{evaluate(parse(bad));}));
        try {evaluate(parse("1/(2-2)"));CHECK(false);}catch(const Error& e){CHECK(e.pos==1);CHECK(e.category=="division by zero");}
        Limits l;l.source=2;CHECK(p4test::throws<Error>([&]{parse("123",l);}));
        l=Limits{};l.tokens=3;CHECK(p4test::throws<Error>([&]{parse("1+2",l);}));
        l.tokens=4;CHECK(evaluate(parse("1+2",l))==3);
        l=Limits{};l.nodes=2;CHECK(p4test::throws<Error>([&]{parse("1+2",l);}));
        l=Limits{};l.depth=2;CHECK(p4test::throws<Error>([&]{parse("1+2+3",l);}));
        std::string deep(65,'(');deep+='1';deep+=std::string(65,')');
        CHECK(p4test::throws<Error>([&]{parse(deep);}));
        std::string chain="1";for(int i=0;i<70;++i)chain+="+1";
        CHECK(p4test::throws<Error>([&]{parse(chain);}));
        for(int a=-10;a<=10;++a)for(int b=1;b<=10;++b) {
            const auto text="("+std::to_string(a)+"+"+std::to_string(b)+")*3";
            CHECK(evaluate(parse(text))==(a+b)*3);
        }

    });
}
