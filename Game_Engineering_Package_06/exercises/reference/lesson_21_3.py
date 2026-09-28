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

def perspective_attribute(weights, values, clip_w):
    """Convex barycentric scalar interpolation; positive finite clip w only."""
    if not (len(weights)==len(values)==len(clip_w)) or not weights:
        raise ValueError('equal nonempty arrays required')
    a=[finite(x,'weight') for x in weights]
    v=[finite(x,'attribute') for x in values]
    w=[finite(x,'w') for x in clip_w]
    if any(x<0 for x in a) or not math.isclose(sum(a),1,abs_tol=1e-9):
        raise ValueError('weights must be nonnegative and sum to one')
    if any(x<=0 for x in w): raise ValueError('w must be positive')
    den=sum(x/y for x,y in zip(a,w))
    return sum(x*z/y for x,z,y in zip(a,v,w))/den
