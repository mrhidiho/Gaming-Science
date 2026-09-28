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

// Build lexer -> located tokens -> owned AST -> evaluator behind this API.
// No eval(), host scripting engine or calls to the supplied reference parser.
// Full grammar, limits, AST inspection and located errors are in the workbook.
std::int64_t evaluate_expression(std::string_view /*source*/) {
    throw std::logic_error("TODO: bounded recursive-descent expression language");
}

int main() { return p4test::run("student_15_2", [] {
    CHECK(evaluate_expression("2+3*4")==14);
    CHECK(evaluate_expression("(2+3)*4")==20);
    CHECK(evaluate_expression("8-3-2")==3);
    CHECK(evaluate_expression("-7/3")==-2);
    CHECK(p4test::throws<std::runtime_error>([]{(void)evaluate_expression("2+)");}));
}); }
