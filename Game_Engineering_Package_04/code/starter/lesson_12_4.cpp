// Student work: this file intentionally compiles but fails until implemented.
// The tests here are a starting contract, NOT the complete lesson acceptance suite.
// Read LAB_WORKBOOK.pdf; add its boundary cases and your independent transfer test.
#include "check.hpp"
#include <algorithm>
#include <concepts>
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

// Add a concept requiring the ordering expressions used by this function.
// Contract: ordered non-NaN values, inclusive interval; reversed bounds are rejected.
template<std::integral T> T bounded(T /*value*/, T /*low*/, T /*high*/) {
    throw std::logic_error("TODO: constrained bounded value");
}

int main() { return p4test::run("student_12_4", [] {
    CHECK(bounded(4,0,10)==4);
    CHECK(bounded(-1,0,10)==0);
    CHECK(bounded(12,0,10)==10);
    CHECK(bounded(3L,0L,2L)==2L);
    CHECK(p4test::throws<std::invalid_argument>([]{ (void)bounded(3,9,1); }));
}); }
