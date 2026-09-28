#include "tick.hpp"
#include <limits>
#include <stdexcept>
int next_tick(int current) {
    if (current == std::numeric_limits<int>::max())
        throw std::overflow_error("tick limit");
    return current + 1;
}
