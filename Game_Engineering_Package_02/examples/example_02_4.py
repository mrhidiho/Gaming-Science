# Worked demonstration for Lesson 02.4.
import math

def advance(position, velocity, dt):
    if not math.isfinite(position) or not math.isfinite(velocity):
        raise ValueError("position and velocity must be finite")
    if not math.isfinite(dt) or dt < 0:
        raise ValueError("dt must be finite and nonnegative")
    result = position + velocity * dt
    if not math.isfinite(result):
        raise ValueError("new position overflow")
    return result

next_position = advance(2.0, -6.0, 0.25)
print("next position:", next_position)
