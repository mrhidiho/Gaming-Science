"""Shared input checks, not reference solutions. Python 3.11+ syntax."""
import math

def number(value, name, minimum=None, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value

def integer(value, name, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be <= {maximum}")
    return value

def nearest_rank(values, p):
    if not values or not 0 < p <= 1:
        raise ValueError("nonempty values and 0 < p <= 1 required")
    return sorted(values)[math.ceil(p * len(values)) - 1]
