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

struct Unit { int id; int hp; };
// Return a VALUE; the returned snapshot must survive later container mutation.
std::optional<Unit> snapshot(std::span<const Unit> /*units*/, int /*id*/) {
    throw std::logic_error("TODO: bounded search and copied optional");
}

int main() { return p4test::run("student_11_3", [] {
    std::vector<Unit> units{{7,100}};
    auto saved = snapshot(units,7);
    CHECK(saved && saved->hp==100);
    units.clear();
    CHECK(saved->hp==100);
    CHECK(!snapshot(units,7));
}); }
