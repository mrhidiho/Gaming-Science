"""Reference kernel for 30.1. Not a complete engine subsystem."""
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
    values=payload['times_ms']; budget=finite(payload['budget_ms'])
    if not isinstance(values,list) or not 1<=len(values)<=100000 or budget<=0:raise ValueError('sample count/budget')
    data=sorted(finite(v) for v in values)
    if data[0]<=0:raise ValueError('positive durations required')
    n=len(data)
    def pct(p):return data[math.ceil(p*n)-1]
    mean=math.fsum(v/n for v in data)
    return {'count':n,'mean_ms':mean,'p50_ms':pct(.5),'p95_ms':pct(.95),'p99_ms':pct(.99),'max_ms':data[-1],'over_budget':sum(v>budget for v in data)}
