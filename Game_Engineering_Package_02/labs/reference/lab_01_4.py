import math

def displacement(speed, dt):
    """Finite numeric speed; finite, nonnegative dt. Return displacement."""
    if not math.isfinite(speed) or not math.isfinite(dt) or dt < 0:
        raise ValueError("speed must be finite; dt must be finite and nonnegative")
    result = speed * dt
    if not math.isfinite(result):
        raise ValueError("displacement overflow")
    return result

def frame_interval_ms(fps):
    """Finite positive frames/second -> milliseconds/frame."""
    if not math.isfinite(fps) or fps <= 0:
        raise ValueError("fps must be finite and positive")
    result = 1000.0 / fps
    if not math.isfinite(result):
        raise ValueError("interval overflow")
    return result
