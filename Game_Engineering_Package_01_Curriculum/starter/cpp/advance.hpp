#pragma once
#include <cmath>
#include <stdexcept>

namespace course {
// Finite inputs/results; dt >= 0. No global state and no I/O.
inline double advance(double position, double velocity, double dt) {
    if (!std::isfinite(position) || !std::isfinite(velocity) || !std::isfinite(dt)) {
        throw std::invalid_argument("all inputs must be finite");
    }
    if (dt < 0.0) {
        throw std::invalid_argument("dt must be nonnegative");
    }
    const double result = position + velocity * dt;
    if (!std::isfinite(result)) {
        throw std::overflow_error("result must be finite");
    }
    return result;
}
} // namespace course
