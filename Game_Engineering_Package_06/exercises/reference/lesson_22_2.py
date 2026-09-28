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

def dispatch_groups(element_count, group_size):
    """Ceiling division. Zero elements require zero workgroups."""
    n=integer(element_count,'element_count'); g=integer(group_size,'group_size',1)
    return (n+g-1)//g
