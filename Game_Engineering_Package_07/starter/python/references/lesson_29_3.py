"""Reference kernel for 29.3. Not a complete engine subsystem."""
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
    initial=payload['initial']; inputs=payload['inputs']; corrections=payload['corrections']; oldest=integer(payload.get('oldest',0))
    if type(initial)is not int or not isinstance(inputs,list) or len(inputs)>10000 or oldest>len(inputs):raise ValueError('history domain')
    def delta(v):
        if type(v)is not int or v not in (-1,0,1):raise ValueError('delta domain')
        return v
    tape=[delta(v) for v in inputs]; states=[initial]
    for v in tape:states.append(states[-1]+v)
    edits={}
    if not isinstance(corrections,list) or len(corrections)>10000:raise ValueError('correction count')
    for row in corrections:
        if not isinstance(row,list) or len(row)!=2:raise ValueError('correction row')
        tick=integer(row[0]); value=delta(row[1])
        if not oldest<=tick<len(tape):raise ValueError('outside retained history')
        if tick in edits and edits[tick]!=value:raise ValueError('conflicting correction')
        edits[tick]=value
    if edits:
        first=min(edits)
        for tick,value in edits.items():tape[tick]=value
        states=states[:first+1]
        for value in tape[first:]:states.append(states[-1]+value)
    return states
