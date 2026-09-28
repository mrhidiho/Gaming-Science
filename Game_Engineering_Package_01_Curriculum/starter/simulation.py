"""A small reference for Lesson 02.4; standard-library Python only."""
from math import isfinite


def _finite_number(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be an int or float, not a boolean or text")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be representable as a finite float") from exc
    if not isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def advance(position: float, velocity: float, dt: float) -> float:
    """Return position + velocity * dt; inputs/result finite and dt >= 0.

    Position and velocity may be negative. No outside state is modified.
    Invalid types raise TypeError; invalid numerical values raise ValueError.
    """
    position = _finite_number(position, "position")
    velocity = _finite_number(velocity, "velocity")
    dt = _finite_number(dt, "dt")
    if dt < 0:
        raise ValueError("dt must be nonnegative")
    result = position + velocity * dt
    if not isfinite(result):
        raise ValueError("result overflowed the finite-number contract")
    return result
