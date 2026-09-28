"""Reference kernel for 28.3. Not a complete engine subsystem."""
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
    tree=payload['tree']; budget=integer(payload['budget']); maximizing=payload.get('maximizing',True)
    if type(maximizing)is not bool:raise ValueError('maximizing must be boolean')
    size=0
    def validate(t,depth=0):
        nonlocal size
        size+=1
        if size>10000 or depth>64:raise ValueError('tree cap')
        if isinstance(t,list):
            if not t:raise ValueError('empty internal node')
            for c in t:validate(c,depth+1)
        else:finite(t,'leaf')
    validate(tree); used=0
    class Exhausted(Exception):pass
    def search(t,maximize,alpha,beta):
        nonlocal used
        if used>=budget:raise Exhausted()
        used+=1
        if not isinstance(t,list):return float(t)
        value=-math.inf if maximize else math.inf
        for child in t:
            v=search(child,not maximize,alpha,beta)
            if maximize:value=max(value,v); alpha=max(alpha,value)
            else:value=min(value,v); beta=min(beta,value)
            if alpha>=beta:break
        return value
    try:return {'value':search(tree,maximizing,-math.inf,math.inf),'nodes':used,'complete':True}
    except Exhausted:return {'value':None,'nodes':used,'complete':False}
