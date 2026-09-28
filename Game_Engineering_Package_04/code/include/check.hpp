#pragma once
#include <cstddef>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>

namespace p4test {
inline std::size_t checks = 0;
inline void check(bool condition, const char* expression,
                  const char* file, int line) {
    ++checks;
    if (!condition)
        throw std::runtime_error(std::string(file) + ":" +
            std::to_string(line) + ": " + expression);
}
template<class Error, class Function>
bool throws(Function&& f) {
    try { std::forward<Function>(f)(); }
    catch (const Error&) { return true; }
    catch (...) { return false; }
    return false;
}
template<class Function>
int run(const char* name, Function&& f) {
    try {
        std::forward<Function>(f)();
        std::cout << "PASS " << name << " checks=" << checks << '\n';
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "FAIL " << name << ": " << e.what() << '\n';
        return 1;
    }
}
}
#define CHECK(...) ::p4test::check(bool(__VA_ARGS__), #__VA_ARGS__, __FILE__, __LINE__)
