"""Reference kernel for 27.4. Not a complete engine subsystem."""
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
    pan=finite(payload['pan']); cutoff=integer(payload.get('min_tick',0))
    if not -1<=pan<=1: raise ValueError('pan domain')
    def parse(rows):
        if not isinstance(rows,list) or len(rows)>4096: raise ValueError('event count')
        out=[]
        for row in rows:
            if not isinstance(row,list) or len(row)!=4 or not isinstance(row[0],str) or not 1<=len(row[0])<=64:
                raise ValueError('event identity')
            key=(row[0],*(integer(v) for v in row[1:]))
            if key[1]>=cutoff: out.append(key)
        return out
    seen=set(parse(payload['seen'])); emitted=[]
    for event in parse(payload['events']):
        if event not in seen: seen.add(event); emitted.append(list(event))
    angle=(pan+1)*math.pi/4
    return {'gains':[math.cos(angle),math.sin(angle)],'emitted':emitted,'retained':[list(e) for e in sorted(seen)]}
