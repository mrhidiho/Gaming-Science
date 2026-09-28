"""Educational contract exercise. Python 3.11+; standard library only."""
import copy
import hashlib
import json
import math

def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value

def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(value)

def choose_context(last_use_serials, completed_serial):
    """Lowest-index reusable context, or None; callers must wait/skip if none."""
    done=integer(completed_serial,'completed')
    uses=[integer(v,'last use') for v in last_use_serials]
    return next((i for i,v in enumerate(uses) if v<=done),None)
