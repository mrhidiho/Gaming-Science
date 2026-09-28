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

template<std::size_t Capacity> class Ring {
    static_assert(Capacity>0);
    // Add fixed array, head and count. This exercise is SINGLE-THREADED.
public:
    bool push(int /*value*/) { throw std::logic_error("TODO: reject on full without mutation"); }
    std::optional<int> pop() { throw std::logic_error("TODO: FIFO, explicit empty"); }
};

int main() { return p4test::run("student_13_2", [] {
    Ring<2> q;
    CHECK(!q.pop());
    CHECK(q.push(1));CHECK(q.push(2));CHECK(!q.push(3));
    CHECK(q.pop()==1);CHECK(q.push(3));
    CHECK(q.pop()==2);CHECK(q.pop()==3);CHECK(!q.pop());
}); }
