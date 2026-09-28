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

def ray_box(origin, direction, box_min, box_max):
    """Return forward-ray (t_enter,t_exit), or None. Direction need not be unit."""
    raise NotImplementedError('Complete exercise 21.4; see LAB_WORKBOOK.pdf')
