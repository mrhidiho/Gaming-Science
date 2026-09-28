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

// Decimal bytes only: no sign, whitespace or suffix; maximum budget is inclusive.
std::optional<std::uint32_t> parse_length(std::string_view /*text*/, std::uint32_t /*budget*/) {
    throw std::logic_error("TODO: validate syntax and range before narrowing");
}

int main() { return p4test::run("student_11_2", [] {
    CHECK(parse_length("0", 10) == 0u);
    CHECK(parse_length("10", 10) == 10u);
    CHECK(!parse_length("11", 10));
    CHECK(!parse_length("-1", 10));
    CHECK(!parse_length("12x", 100));
    CHECK(!parse_length("4294967296", std::numeric_limits<std::uint32_t>::max()));
}); }
