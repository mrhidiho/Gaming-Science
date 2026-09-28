"""Reference kernel for 26.4. Not a complete engine subsystem."""
from __future__ import annotations
import math

def finite(value: object, name: str = "value") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number, not a boolean")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def integer(value: object, name: str = "value", minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value

def canonical(state: object) -> bytes:
    import json
    def check(x,depth=0):
        if depth>32: raise ValueError('state nesting cap')
        if isinstance(x,dict):
            if not all(isinstance(k,str) for k in x): raise ValueError('string keys required')
            for v in x.values(): check(v,depth+1)
        elif isinstance(x,list):
            for v in x: check(v,depth+1)
        elif isinstance(x,float): finite(x)
        elif x is not None and type(x) not in (str,int,bool): raise ValueError('unsupported state type')
    check(state)
    try: data=json.dumps(state,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    except (TypeError,ValueError,OverflowError) as exc: raise ValueError('invalid state') from exc
    if len(data)>1000000: raise ValueError('state byte cap')
    return data

def solve(payload: dict) -> int | None:
    import hashlib
    left,right=payload['left'],payload['right']
    if not isinstance(left,list) or not isinstance(right,list) or max(len(left),len(right))>10000:
        raise ValueError('trace length')
    a=[hashlib.sha256(canonical(s)).digest() for s in left]
    b=[hashlib.sha256(canonical(s)).digest() for s in right]
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y: return i
    return min(len(a),len(b)) if len(a)!=len(b) else None
