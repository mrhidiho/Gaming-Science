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

def drawable_extent(width, height, scale, limit):
    """CSS-size model: floor(width*scale); zero suspends, positive clamps to limit."""
    w=finite(width,'width'); h=finite(height,'height'); s=finite(scale,'scale')
    integer(limit,'limit',1)
    if w<0 or h<0 or s<=0: raise ValueError('invalid extent or scale')
    if w==0 or h==0: return None
    a,b=w*s,h*s
    if not math.isfinite(a) or not math.isfinite(b): raise ValueError('extent overflow')
    return max(1,min(limit,math.floor(a))),max(1,min(limit,math.floor(b)))
