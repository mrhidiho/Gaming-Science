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

struct Edge { std::size_t to; std::int64_t cost; };
using Graph=std::vector<std::vector<Edge>>;
std::optional<std::int64_t> shortest_cost(
    const Graph& /*g*/, std::size_t /*start*/, std::size_t /*goal*/) {
    throw std::logic_error("TODO: Dijkstra with checked cost and stale-entry handling");
}

int main() { return p4test::run("student_14_3", [] {
    Graph g{{{1,10},{2,1}},{},{{1,1}}, {}};
    CHECK(shortest_cost(g,0,1)==2);
    CHECK(shortest_cost(g,0,0)==0);
    CHECK(!shortest_cost(g,0,3));
    g[0][0].cost=-1;
    CHECK(p4test::throws<std::invalid_argument>([&]{(void)shortest_cost(g,0,1);}));
}); }
