"""Reference kernel for 28.1. Not a complete engine subsystem."""
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
    import heapq
    grid=payload['grid']; budget=integer(payload['budget'])
    if not isinstance(grid,list) or not 1<=len(grid)<=128 or not all(isinstance(r,str) for r in grid): raise ValueError('grid')
    h=len(grid); w=len(grid[0])
    if not 1<=w<=128 or any(len(r)!=w or set(r)-set('.#') for r in grid): raise ValueError('rectangular grid')
    def point(value):
        if not isinstance(value,list) or len(value)!=2 or any(type(v)is not int for v in value): raise ValueError('point')
        x,y=value
        if not 0<=x<w or not 0<=y<h: raise ValueError('point bounds')
        return x,y
    start,goal=point(payload['start']),point(payload['goal'])
    if grid[start[1]][start[0]]=='#' or grid[goal[1]][goal[0]]=='#':
        return {'status':'unreachable','path':[],'expanded':0}
    def heuristic(p):return abs(p[0]-goal[0])+abs(p[1]-goal[1])
    frontier=[(heuristic(start),0,start)]; cost={start:0}; parent={}; expanded=0
    while frontier:
        _,g,p=heapq.heappop(frontier)
        if g!=cost.get(p): continue
        if expanded>=budget:return {'status':'budget_exhausted','path':[],'expanded':expanded}
        expanded+=1
        if p==goal:
            path=[p]
            while path[-1]!=start:path.append(parent[path[-1]])
            return {'status':'found','path':[list(v) for v in reversed(path)],'expanded':expanded}
        x,y=p
        for q in ((x-1,y),(x,y-1),(x,y+1),(x+1,y)):
            qx,qy=q
            if 0<=qx<w and 0<=qy<h and grid[qy][qx]!='#' and g+1<cost.get(q,float('inf')):
                cost[q]=g+1; parent[q]=p; heapq.heappush(frontier,(g+1+heuristic(q),g+1,q))
    return {'status':'unreachable','path':[],'expanded':expanded}
