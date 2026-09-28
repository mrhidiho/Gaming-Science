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

// Implement your own collision policy; do not wrap std::unordered_map as the answer.
class IntMap {
public:
    bool insert(int /*key*/, int /*value*/) { throw std::logic_error("TODO: insert true, update false"); }
    std::optional<int> find(int /*key*/) const { throw std::logic_error("TODO: lookup"); }
    bool erase(int /*key*/) { throw std::logic_error("TODO: preserve collision search"); }
};

int main() { return p4test::run("student_13_3", [] {
    IntMap map;
    CHECK(map.insert(1,10));CHECK(map.insert(2,20));
    CHECK(!map.insert(1,30));CHECK(map.find(1)==30);
    CHECK(map.erase(1));CHECK(!map.find(1));CHECK(map.find(2)==20);
    CHECK(!map.erase(999));
}); }
