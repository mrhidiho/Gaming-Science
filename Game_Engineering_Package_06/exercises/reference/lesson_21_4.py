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
    if any(len(v)!=3 for v in (origin,direction,box_min,box_max)):
        raise ValueError('three-dimensional arguments required')
    o,d,lo,hi=([finite(x,'coordinate') for x in v] for v in (origin,direction,box_min,box_max))
    if not any(x!=0 for x in d): raise ValueError('zero direction')
    if any(a>b for a,b in zip(lo,hi)): raise ValueError('inverted box')
    enter,leave=0.0,float('inf')
    for p,v,a,b in zip(o,d,lo,hi):
        if v==0:
            if p<a or p>b: return None
            continue
        x,y=sorted(((a-p)/v,(b-p)/v))
        enter=max(enter,x); leave=min(leave,y)
        if enter>leave: return None
    return enter,leave
