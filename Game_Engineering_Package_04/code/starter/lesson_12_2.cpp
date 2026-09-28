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

// Narrow exercise: a replacement operation with the strong guarantee.
// Then implement the move-only owner required by the full lesson.
void replace(std::unique_ptr<int>& /*destination*/, int /*value*/, bool /*fail*/) {
    throw std::logic_error("TODO: prepare candidate, then commit without throwing");
}

int main() { return p4test::run("student_12_2", [] {
    auto value=std::make_unique<int>(7);
    auto* original=value.get();
    CHECK(p4test::throws<std::runtime_error>([&]{replace(value,9,true);}));
    CHECK(value.get()==original && *value==7);
    replace(value,9,false);
    CHECK(*value==9);
}); }
