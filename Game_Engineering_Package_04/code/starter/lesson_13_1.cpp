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

// Educational int-only buffer; do not generalize object lifetime yet.
class IntBuffer {
public:
    void push(int /*value*/) { throw std::logic_error("TODO: grow with allocate-copy-commit"); }
    std::size_t size() const { throw std::logic_error("TODO: logical size"); }
    int at(std::size_t /*index*/) const { throw std::logic_error("TODO: bounds check"); }
    // Add capacity/moved counters, invariants and explicit copy/move policy.
};

int main() { return p4test::run("student_13_1", [] {
    IntBuffer b;
    CHECK(b.size()==0);
    for(int i=0;i<100;++i)b.push(i);
    CHECK(b.size()==100);
    CHECK(b.at(99)==99);
    CHECK(p4test::throws<std::out_of_range>([&]{(void)b.at(100);}));
}); }
