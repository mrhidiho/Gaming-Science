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

def clip_near(polygon):
    """Sutherland-Hodgman z>=0 clip. Vertices are finite (x,y,z,w) tuples."""
    raise NotImplementedError('Complete exercise 21.2; see LAB_WORKBOOK.pdf')
