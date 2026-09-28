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

struct Counts { int live=0; int acquired=0; int released=0; };
class Owner {
    // Store the borrowed Counts pointer. It must outlive this owner.
public:
    explicit Owner(Counts& /*counts*/) { throw std::logic_error("TODO: acquire one mock resource"); }
    ~Owner() noexcept { /* TODO: release exactly once */ }
    Owner(const Owner&)=delete;
    Owner& operator=(const Owner&)=delete;
};
void use_then_fail(Counts& counts) { Owner resource(counts); throw std::runtime_error("injected"); }

int main() { return p4test::run("student_12_1", [] {
    Counts counts;
    { Owner a(counts); CHECK(counts.live==1); }
    CHECK(counts.live==0 && counts.acquired==counts.released);
    CHECK(p4test::throws<std::runtime_error>([&]{use_then_fail(counts);}));
    CHECK(counts.live==0 && counts.acquired==counts.released);
}); }
