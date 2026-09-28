"""Reference kernel for 26.2. Not a complete engine subsystem."""
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

def solve(payload: dict) -> dict:
    va,vb,wa,wb,e=[finite(payload[k],k) for k in ('va','vb','wa','wb','e')]
    if min(wa,wb)<0 or not 0<=e<=1: raise ValueError('mass/restitution domain')
    vn=vb-va; k=wa+wb
    j=0.0 if vn>=0 or k==0 else -(1+e)*vn/k
    result={'va':va-j*wa,'vb':vb+j*wb,'impulse':j}
    if not all(math.isfinite(v) for v in result.values()): raise ValueError('overflow')
    return result
