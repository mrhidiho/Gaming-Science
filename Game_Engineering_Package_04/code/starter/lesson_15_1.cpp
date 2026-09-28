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

enum class Type { Number, Boolean };
// Type rule exercise: arithmetic addition accepts numbers only.
Type add_type(Type /*left*/,Type /*right*/) {
    throw std::logic_error("TODO: reject Boolean arithmetic before evaluation");
}
std::int64_t damage(std::int64_t /*hp*/,std::int64_t /*incoming*/,std::int64_t /*armor*/) {
    throw std::logic_error("TODO: pure bounded damage function");
}

int main() { return p4test::run("student_15_1", [] {
    CHECK(add_type(Type::Number,Type::Number)==Type::Number);
    CHECK(p4test::throws<std::invalid_argument>([]{(void)add_type(Type::Number,Type::Boolean);}));
    CHECK(damage(10,7,2)==5);
    CHECK(damage(10,1,2)==10);
    CHECK(damage(10,100,0)==0);
}); }
