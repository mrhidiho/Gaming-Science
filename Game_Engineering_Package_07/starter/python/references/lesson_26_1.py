"""Reference kernel for 26.1. Not a complete engine subsystem."""
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
    from itertools import combinations
    size = finite(payload['cell_size'], 'cell_size')
    if size <= 0: raise ValueError('positive cell_size required')
    circles = payload['circles']
    if not isinstance(circles, list) or len(circles) > 512: raise ValueError('circle count')
    items = {}; cells = {}
    for row in circles:
        if not isinstance(row, list) or len(row) != 4: raise ValueError('circle row')
        ident = integer(row[0], 'id')
        if ident in items: raise ValueError('duplicate id')
        x,y,r = [finite(z) for z in row[1:]]
        if r <= 0: raise ValueError('positive radius required')
        bounds = [(x-r)/size,(x+r)/size,(y-r)/size,(y+r)/size]
        if not all(math.isfinite(z) for z in bounds): raise ValueError('bounds overflow')
        x0,x1,y0,y1 = [math.floor(z) for z in bounds]
        if (x1-x0+1)*(y1-y0+1) > 4096: raise ValueError('cell coverage cap')
        items[ident]=(x,y,r)
        for gx in range(x0,x1+1):
            for gy in range(y0,y1+1): cells.setdefault((gx,gy),[]).append(ident)
    pairs=set()
    for members in cells.values():
        pairs.update(tuple(sorted(pair)) for pair in combinations(members,2))
    contacts=[]
    for a,b in sorted(pairs):
        ax,ay,ar=items[a]; bx,by,br=items[b]
        # hypot is more overflow-resistant than naive squared distances.
        if math.hypot(bx-ax,by-ay) <= ar+br: contacts.append([a,b])
    return {'candidates':[list(p) for p in sorted(pairs)],'contacts':contacts}
