"""Reference kernel for 30.2. Not a complete engine subsystem."""
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
    import re
    text=payload['text']; bindings=payload['bindings']; action=payload['action']
    if not isinstance(text,str) or len(text)>4096 or not isinstance(bindings,dict) or len(bindings)>64:raise ValueError('text/bindings')
    if not all(isinstance(k,str) and k and isinstance(v,str) and v and len(v)<=64 for k,v in bindings.items()):raise ValueError('binding names')
    if not isinstance(action,str) or action not in bindings or len(set(bindings.values()))!=len(bindings):raise ValueError('missing/conflicting binding')
    pattern=r'(\{[A-Za-z_][A-Za-z_0-9]*\})'
    remainder=re.sub(pattern,'',text)
    if '{' in remainder or '}' in remainder:raise ValueError('malformed placeholder')
    pieces=re.split(pattern,text); out=[]
    for i,piece in enumerate(pieces):
        out.append(piece if i%2 else ''.join(c*2 if c in 'aeiouAEIOU' else c for c in piece))
    return {'text':'['+''.join(out)+']','prompt':'Press '+bindings[action]}
