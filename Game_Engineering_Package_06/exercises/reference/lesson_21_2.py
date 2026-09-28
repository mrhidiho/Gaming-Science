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
    pts=[]
    for p in polygon:
        if len(p)!=4: raise ValueError('vertex requires four components')
        pts.append(tuple(finite(x,'component') for x in p))
    if not pts: return []
    out=[]
    prev=pts[-1]
    for cur in pts:
        dp,dc=prev[2],cur[2]
        if (dp>=0)!=(dc>=0):
            t=dp/(dp-dc)
            hit=tuple(a+t*(b-a) for a,b in zip(prev,cur))
            if not out or hit!=out[-1]: out.append(hit)
        if dc>=0 and (not out or cur!=out[-1]): out.append(cur)
        prev=cur
    if len(out)>1 and out[0]==out[-1]: out.pop()
    return out
