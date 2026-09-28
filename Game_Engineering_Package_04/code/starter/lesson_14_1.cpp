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

// Precondition: ascending sorted range. Return first index where a[index]>=target.
std::size_t lower_bound_index(std::span<const int> /*a*/, int /*target*/) {
    throw std::logic_error("TODO: half-open search and invariant");
}

int main() { return p4test::run("student_14_1", [] {
    const std::vector<int> a{1,3,3,8};
    CHECK(lower_bound_index(a,0)==0);
    CHECK(lower_bound_index(a,3)==1);
    CHECK(lower_bound_index(a,4)==3);
    CHECK(lower_bound_index(a,9)==4);
    CHECK(lower_bound_index({},2)==0);
}); }
