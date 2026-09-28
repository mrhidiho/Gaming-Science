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

// First implement this; then split declaration and definition into your own .hpp/.cpp.
// Add the new .cpp with target_sources(student_11_1 ...) in code/CMakeLists.txt.
int next_tick(int /*tick*/) { throw std::logic_error("TODO: checked next_tick"); }

int main() { return p4test::run("student_11_1", [] {
    CHECK(next_tick(0) == 1);
    CHECK(next_tick(41) == 42);
    CHECK(p4test::throws<std::overflow_error>([]{ (void)next_tick(std::numeric_limits<int>::max()); }));
}); }
