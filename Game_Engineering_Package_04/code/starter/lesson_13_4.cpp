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

class MinHeap {
    std::vector<int> values_;
public:
    void push(int /*value*/) { throw std::logic_error("TODO: append and sift up"); }
    std::optional<int> pop() { throw std::logic_error("TODO: root replacement and sift down"); }
};

int main() { return p4test::run("student_13_4", [] {
    MinHeap heap;
    CHECK(!heap.pop());
    for(int x:{4,1,7,1,-2})heap.push(x);
    for(int expected:{-2,1,1,4,7})CHECK(heap.pop()==expected);
    CHECK(!heap.pop());
}); }
