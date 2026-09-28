#include "advance.hpp"
#include <iomanip>
#include <iostream>

int main() {
    double position = 0.0;
    std::cout << std::fixed << std::setprecision(2);
    for (int tick = 1; tick <= 5; ++tick) {
        position = course::advance(position, 6.0, 0.25);
        std::cout << "tick " << tick << ": x=" << position << " units\n";
    }
    return 0;
}
