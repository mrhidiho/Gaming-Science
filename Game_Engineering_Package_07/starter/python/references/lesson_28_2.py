"""Reference kernel for 28.2. Not a complete engine subsystem."""
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
    margin=finite(payload['margin']); raw=payload['scores']; current=payload.get('current')
    if margin<0 or not isinstance(raw,dict) or len(raw)>256: raise ValueError('selector domain')
    if current is not None and not isinstance(current,str): raise ValueError('current action')
    scores={}
    for name,value in raw.items():
        if not isinstance(name,str) or not 1<=len(name)<=64: raise ValueError('action name')
        if value is not None:scores[name]=finite(value)
    if not scores:return {'action':None,'reason':'no_valid_action'}
    best=min(scores,key=lambda name:(-scores[name],name))
    if current in scores and scores[best]<=scores[current]+margin:
        return {'action':current,'reason':'retained'}
    return {'action':best,'reason':'selected'}
