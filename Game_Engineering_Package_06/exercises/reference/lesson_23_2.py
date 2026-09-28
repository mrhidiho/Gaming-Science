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

def mip_texels(width, height):
    """Sum floor-halved mip extents including base and final 1x1 level."""
    w=integer(width,'width',1); h=integer(height,'height',1); total=0
    while True:
        total+=w*h
        if w==1 and h==1: return total
        w=max(1,w//2); h=max(1,h//2)
