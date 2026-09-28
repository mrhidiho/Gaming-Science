import math

def advance(position, velocity, dt):
    """Finite numeric inputs; dt >= 0; return a finite new position.

    Does not print, read input or change external state.
    """
    if not all(math.isfinite(v) for v in (position, velocity, dt)):
        raise ValueError("all inputs must be finite")
    if dt < 0:
        raise ValueError("dt must be nonnegative")
    result = position + velocity * dt
    if not math.isfinite(result):
        raise ValueError("new position overflow")
    return result
