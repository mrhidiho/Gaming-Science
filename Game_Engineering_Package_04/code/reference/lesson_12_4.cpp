// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include <concepts>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <vector>


template<std::integral T>T clamp_int(T value,T low,T high) {
    if(high<low) throw std::invalid_argument("reversed bounds");
    return value<low?low:(high<value?high:value);
}
template<class T>concept Clampable=requires(T x){clamp_int(x,x,x);};
struct Cell { std::int64_t x=0,vx=1,y=0,vy=1; };

int main() {
    return p4test::run("12.4", [] {

        static_assert(Clampable<int>);static_assert(!Clampable<double>);
        CHECK(clamp_int(12,0,10)==10);CHECK(clamp_int(-3,0,10)==0);
        CHECK(clamp_int(5,0,10)==5);CHECK(clamp_int(8,4,4)==4);
        CHECK(p4test::throws<std::invalid_argument>([]{clamp_int(2,10,0);}));
        for(std::size_t n:{0u,1u,17u,1000u}) {
            std::vector<Cell> aos(n);std::vector<std::int64_t> x(n,0),vx(n,1);
            for(int step=0;step<10;++step) {
                for(auto& cell:aos) cell.x+=cell.vx;
                for(std::size_t i=0;i<n;++i) x[i]+=vx[i];
            }
            std::int64_t ca=0,cs=0;
            for(std::size_t i=0;i<n;++i) { CHECK(aos[i].x==x[i]);ca+=aos[i].x;cs+=x[i]; }
            CHECK(ca==cs);CHECK(ca==static_cast<std::int64_t>(n)*10);
        }
        std::cout<<"Use layout_benchmark in a Release build for CSV timings.\n";

    });
}
