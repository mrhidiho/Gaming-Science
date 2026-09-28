#include "advance.hpp"
#include <cmath>
#include <iostream>
#include <limits>
#include <string>

int failures = 0;
void check(bool condition, const std::string& name) {
    if (!condition) { std::cerr << "FAIL: " << name << '\n'; ++failures; }
}
template<class Exception, class Function>
void expect_throw(Function function, const std::string& name) {
    try { function(); check(false, name + " (no exception)"); }
    catch (const Exception&) { }
    catch (...) { check(false, name + " (wrong exception)"); }
}
int main() {
    check(course::advance(2, 8, .25) == 4, "positive motion");
    check(course::advance(2, -8, .25) == 0, "negative velocity");
    check(course::advance(2, 8, 0) == 2, "zero time");
    check(course::advance(-2, 0, .25) == -2, "stationary");
    double position=0;
    for (int i=0; i<5; ++i) position=course::advance(position, 6, .25);
    check(position == 7.5, "five ticks");
    check(std::abs(course::advance(.1,.2,.3)-.16) < 1e-12, "decimal tolerance");
    expect_throw<std::invalid_argument>([]{course::advance(0,1,-.1);}, "negative time");
    const double nan=std::numeric_limits<double>::quiet_NaN();
    const double inf=std::numeric_limits<double>::infinity();
    for (double invalid : {nan, inf, -inf}) {
        expect_throw<std::invalid_argument>([=]{course::advance(invalid,1,.1);}, "invalid position");
        expect_throw<std::invalid_argument>([=]{course::advance(0,invalid,.1);}, "invalid velocity");
        expect_throw<std::invalid_argument>([=]{course::advance(0,1,invalid);}, "invalid dt");
    }
    expect_throw<std::overflow_error>([]{course::advance(1e308,1e308,1e308);}, "overflow");
    if (failures == 0) std::cout << "All motion-contract checks passed.\n";
    return failures == 0 ? 0 : 1;
}
