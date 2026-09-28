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

using Graph=std::vector<std::vector<std::size_t>>;
std::optional<std::vector<std::size_t>> breadth_first_path(
    const Graph& /*g*/, std::size_t /*start*/, std::size_t /*goal*/) {
    throw std::logic_error("TODO: validate, FIFO frontier, visited-on-discovery, parents");
}

int main() { return p4test::run("student_14_2", [] {
    Graph g{{1,2},{3},{3},{},{}};
    auto path=breadth_first_path(g,0,3);
    CHECK(path && *path==std::vector<std::size_t>({0,1,3}));
    CHECK(!breadth_first_path(g,0,4));
    CHECK(breadth_first_path(g,0,0)==std::vector<std::size_t>({0}));
    CHECK(p4test::throws<std::out_of_range>([&]{(void)breadth_first_path(g,0,5);}));
}); }
