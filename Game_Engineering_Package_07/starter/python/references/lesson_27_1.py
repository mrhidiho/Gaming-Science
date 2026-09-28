"""Reference kernel for 27.1. Not a complete engine subsystem."""
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

def solve(payload: dict) -> list:
    parents,local=payload['parents'],payload['local']
    if not isinstance(parents,list) or not isinstance(local,list) or len(parents)!=len(local) or len(local)>256:
        raise ValueError('hierarchy size')
    n=len(local); poses=[]
    for p,row in zip(parents,local):
        if type(p) is not int or not -1<=p<n or not isinstance(row,list) or len(row)!=3: raise ValueError('joint data')
        poses.append(tuple(finite(v) for v in row))
    state=[0]*n; world=[None]*n
    def visit(i):
        if state[i]==1: raise ValueError('hierarchy cycle')
        if state[i]==2: return world[i]
        state[i]=1; x,y,a=poses[i]; parent=parents[i]
        if parent>=0:
            px,py,pa=visit(parent); c,s=math.cos(pa),math.sin(pa)
            x,y,a=px+c*x-s*y,py+s*x+c*y,pa+a
        if not all(math.isfinite(v) for v in (x,y,a)): raise ValueError('transform overflow')
        world[i]=[x,y,a]; state[i]=2; return world[i]
    for i in range(n): visit(i)
    return world
