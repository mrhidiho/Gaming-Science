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

enum class Op { Push, Neg, Add, Sub, Mul, Div };
struct Instruction { Op op; std::int64_t value=0; std::size_t offset=0; };
std::int64_t execute(std::span<const Instruction> /*code*/,std::size_t /*fuel*/) {
    throw std::logic_error("TODO: checked stack, opcode, operand, range and instruction budgets");
}

int main() { return p4test::run("student_15_3", [] {
    const std::vector<Instruction> program{{Op::Push,8},{Op::Push,3},{Op::Sub}};
    CHECK(execute(program,3)==5);
    CHECK(p4test::throws<std::runtime_error>([&]{(void)execute(program,2);}));
    CHECK(p4test::throws<std::runtime_error>([]{(void)execute(std::vector<Instruction>{{Op::Add}},5);}));
    CHECK(p4test::throws<std::runtime_error>([]{(void)execute(std::vector<Instruction>{{Op::Push,1},{Op::Push,0},{Op::Div}},5);}));
}); }
