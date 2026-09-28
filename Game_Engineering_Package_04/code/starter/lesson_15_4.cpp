// Student contract. Implement the recognizer; extend your 15.2/15.3 optimizer.
#include "check.hpp"
#include <stdexcept>
#include <string_view>
bool decimal_fsm(std::string_view /*text*/) {
    throw std::logic_error("TODO: Start/Digits/Dead finite-state recognizer");
}
// Also implement checked constant folding in your compiler. Preserve source
// errors: (1/0)*0 must still report the original division-by-zero location.
int main() { return p4test::run("student_15_4", [] {
    CHECK(!decimal_fsm(""));
    CHECK(decimal_fsm("007"));
    CHECK(decimal_fsm("7"));
    CHECK(!decimal_fsm("7x"));
    CHECK(!decimal_fsm(" 7"));
    CHECK(!decimal_fsm("-7"));
}); }
