// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "algorithms.hpp"
#include <algorithm>
#include <functional>
#include <random>
#include <utility>
#include <vector>


int main() {
    return p4test::run("14.1", [] {

        for(std::vector<int> input:std::vector<std::vector<int>>{{},{4},{1,4,4,9},{9,8,7,6},{2,1,2}}) {
            auto expected=input;std::sort(expected.begin(),expected.end());
            auto a=input,b=input;ge::insertion_sort(a,std::less<int>{});ge::merge_sort(b,std::less<int>{});
            CHECK(a==expected);CHECK(b==expected);
            for(int x=-1;x<12;++x) {
                const auto pos=static_cast<std::size_t>(std::lower_bound(expected.begin(),expected.end(),x)-expected.begin());
                CHECK(ge::lower_bound_index(expected,x)==pos);
            }
        }
        using Record=std::pair<int,int>;std::vector<Record> records{{2,0},{1,1},{2,2},{1,3}};
        auto less=[](const Record& a,const Record& b){return a.first<b.first;};
        const std::vector<Record> stable{{1,1},{1,3},{2,0},{2,2}};
        auto a=records,b=records;ge::insertion_sort(a,less);ge::merge_sort(b,less);CHECK(a==stable);CHECK(b==stable);
        std::mt19937 rng(1401);
        for(int trial=0;trial<100;++trial) {
            std::vector<int> input(100);for(auto& x:input)x=static_cast<int>(rng()%31);
            auto expected=input;std::sort(expected.begin(),expected.end());
            a.clear(); // records are unrelated to this integer test
            auto x=input,y=input;ge::insertion_sort(x,std::less<int>{});ge::merge_sort(y,std::less<int>{});
            CHECK(x==expected);CHECK(y==expected);
        }

    });
}
