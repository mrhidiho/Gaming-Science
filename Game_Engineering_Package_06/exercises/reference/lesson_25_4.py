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

def nearest_rank(samples, percentile):
    """Nearest-rank quantile, p in (0,100]; nonnegative finite timings required."""
    p=finite(percentile,'percentile')
    if not 0<p<=100: raise ValueError('percentile must be in (0,100]')
    values=[finite(v,'sample') for v in samples]
    if not values or any(v<0 for v in values): raise ValueError('nonempty nonnegative samples required')
    return sorted(values)[math.ceil(p*len(values)/100)-1]
