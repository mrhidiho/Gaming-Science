"""Reference kernel for 29.2. Not a complete engine subsystem."""
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

def solve(payload: dict) -> float:
    import bisect
    t=finite(payload['time']); raw=payload['snapshots']
    if not isinstance(raw,list) or not 1<=len(raw)<=4096:raise ValueError('snapshot count')
    unique={}
    for row in raw:
        if not isinstance(row,list) or len(row)!=2:raise ValueError('snapshot row')
        st,x=finite(row[0]),finite(row[1])
        if st in unique and unique[st]!=x:raise ValueError('conflicting timestamp')
        unique[st]=x
    times=sorted(unique)
    if t<=times[0]:return unique[times[0]]
    if t>=times[-1]:return unique[times[-1]]
    hi=bisect.bisect_right(times,t); t0,t1=times[hi-1],times[hi]
    alpha=(t-t0)/(t1-t0)
    out=(1-alpha)*unique[t0]+alpha*unique[t1]
    if not math.isfinite(out):raise ValueError('interpolation overflow')
    return out
