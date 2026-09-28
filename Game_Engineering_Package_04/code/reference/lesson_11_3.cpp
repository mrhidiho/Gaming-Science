// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "model.hpp"
#include <vector>


int by_value(int x) { return x+1; } // test domain is small integers
int by_const_ref(const int& x) { return x; }
std::optional<int> by_pointer(const int* x) {
    if(x==nullptr) return std::nullopt;
    return *x;
}
// Do not execute: const int& bad() { int local=7; return local; }
// The referred-to local dies at return. Repair by returning an int value.

int main() {
    return p4test::run("11.3", [] {

        std::vector<ge::Unit> units;
        CHECK(!ge::position_of(units,7));CHECK(!ge::hp_of(nullptr));
        units.push_back({7,{2,3},10});
        const auto copy=ge::position_of(units,7);
        CHECK(copy==ge::Position{2,3});CHECK(ge::hp_of(&units[0])==10);
        CHECK(!ge::position_of(units,999));
        const auto old_capacity=units.capacity();units.reserve(old_capacity+100);
        CHECK(copy==ge::Position{2,3}); // value survives reallocation
        units.clear();CHECK(copy==ge::Position{2,3});
        int original=4;CHECK(by_value(original)==5);CHECK(original==4);
        CHECK(by_const_ref(original)==4);CHECK(by_pointer(&original)==4);
        CHECK(!by_pointer(nullptr));

    });
}
