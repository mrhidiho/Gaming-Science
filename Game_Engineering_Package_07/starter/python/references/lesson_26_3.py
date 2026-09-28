"""Reference kernel for 26.3. Not a complete engine subsystem."""
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

def solve(payload: dict) -> float | None:
    x,v,lo,hi,dt=[finite(payload[k],k) for k in ('x','v','lo','hi','dt')]
    if lo>hi or dt<0: raise ValueError('invalid interval')
    if lo<=x<=hi: return 0.0
    if v==0: return None
    t0,t1=sorted(((lo-x)/v,(hi-x)/v))
    entry=max(0.0,t0); exit=min(dt,t1)
    return entry if entry<=exit else None
