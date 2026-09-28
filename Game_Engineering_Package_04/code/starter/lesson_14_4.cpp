// Student work: this file intentionally compiles but fails until implemented.
// The tests here are a starting contract, NOT the complete lesson acceptance suite.
// Read LAB_WORKBOOK.pdf; add its boundary cases and your independent transfer test.
#include "check.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <limits>
#include <memory>
#include <optional>
#include <queue>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

struct Item { std::size_t weight; std::int64_t value; };
std::int64_t knapsack(std::span<const Item> /*items*/, std::size_t /*budget*/) {
    throw std::logic_error("TODO: bounded 0/1 DP; descending capacity");
}

int main() { return p4test::run("student_14_4", [] {
    const std::vector<Item> items{{2,3},{3,4},{4,5}};
    CHECK(knapsack(items,5)==7);
    CHECK(knapsack(items,0)==0);
    CHECK(knapsack({},5)==0);
    CHECK(knapsack(std::vector<Item>{{2,3}},4)==3);
}); }
