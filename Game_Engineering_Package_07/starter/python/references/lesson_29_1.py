"""Reference kernel for 29.1. Not a complete engine subsystem."""
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
    x=payload['position']; ack=integer(payload['ack']); pending=payload['pending']
    if type(x)is not int or not -100<=x<=100 or not isinstance(pending,list) or len(pending)>4096:
        raise ValueError('state/history domain')
    unique={}
    for row in pending:
        if not isinstance(row,list) or len(row)!=2:raise ValueError('input row')
        seq=integer(row[0]); delta=row[1]
        if type(delta)is not int or delta not in (-1,0,1):raise ValueError('illegal movement')
        if seq in unique and unique[seq]!=delta:raise ValueError('conflicting duplicate')
        unique[seq]=delta
    remaining=[[seq,delta] for seq,delta in sorted(unique.items()) if seq>ack]
    for _,delta in remaining:x=max(-100,min(100,x+delta))
    return {'position':x,'pending':remaining}
