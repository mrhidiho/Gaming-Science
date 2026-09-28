"""Reference kernel for 27.2. Not a complete engine subsystem."""
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
    l1,l2,x,y=[finite(payload[k],k) for k in ('l1','l2','x','y')]
    if not (0<l1<=1000 and 0<l2<=1000): raise ValueError('length domain')
    d=math.hypot(x,y)
    if not math.isfinite(d): raise ValueError('target overflow')
    lo,hi=abs(l1-l2),l1+l2; reachable=lo<=d<=hi
    dc=min(hi,max(lo,d)); direction=math.atan2(y,x) if d else 0.0
    c2=(dc*dc-l1*l1-l2*l2)/(2*l1*l2)
    elbow=math.acos(max(-1.0,min(1.0,c2)))
    shoulder=direction-math.atan2(l2*math.sin(elbow),l1+l2*math.cos(elbow))
    if dc==0: shoulder=0.0
    end=[l1*math.cos(shoulder)+l2*math.cos(shoulder+elbow),
         l1*math.sin(shoulder)+l2*math.sin(shoulder+elbow)]
    return {'shoulder':shoulder,'elbow':elbow,'endpoint':end,'reachable':reachable}
