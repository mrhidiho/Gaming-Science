// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "algorithms.hpp"
#include <random>
#include <stdexcept>
#include <vector>


int main() {
    return p4test::run("14.4", [] {

        CHECK(ge::knapsack({},0)==0);CHECK(ge::knapsack({},10)==0);
        CHECK(ge::knapsack(std::vector<ge::Item>{{2,3},{3,4},{4,5}},5)==7);
        CHECK(ge::knapsack(std::vector<ge::Item>{{2,3}},4)==3);
        CHECK(ge::knapsack(std::vector<ge::Item>{{9,99}},2)==0);
        CHECK(p4test::throws<std::invalid_argument>([]{ge::knapsack(std::vector<ge::Item>{{0,1}},5);}));
        CHECK(p4test::throws<std::length_error>([]{ge::knapsack({},10001);}));
        std::mt19937 rng(1404);
        for(int trial=0;trial<250;++trial) {
            std::vector<ge::Item> items;const auto n=rng()%9;
            for(std::size_t i=0;i<n;++i)items.push_back({1+rng()%9,static_cast<std::int64_t>(rng()%20)});
            const std::size_t budget=rng()%21;
            CHECK(ge::knapsack(items,budget)==ge::knapsack_brute(items,budget));
        }

    });
}
