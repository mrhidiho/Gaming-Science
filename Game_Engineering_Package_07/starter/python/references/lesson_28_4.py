"""Reference kernel for 28.4. Not a complete engine subsystem."""
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

def sigmoid(z: float) -> float:
    if z>=0:return 1/(1+math.exp(-z))
    e=math.exp(z); return e/(1+e)

def solve(payload: dict) -> dict:
    x=[finite(v) for v in payload['x']]; w=[finite(v) for v in payload['w']]
    b=finite(payload['b']); lr=finite(payload['lr']); y=payload['y']
    if not 1<=len(x)<=64 or len(w)!=len(x) or type(y)is not int or y not in (0,1) or not 0<lr<=1:
        raise ValueError('learning domain')
    z=sum(a*c for a,c in zip(w,x))+b
    if not math.isfinite(z):raise ValueError('logit overflow')
    p=sigmoid(z); error=p-y
    new_w=[a-lr*error*c for a,c in zip(w,x)]; new_b=b-lr*error
    if not all(math.isfinite(v) for v in new_w+[new_b]):raise ValueError('parameter overflow')
    return {'w':new_w,'b':new_b,'probability_before':p}
