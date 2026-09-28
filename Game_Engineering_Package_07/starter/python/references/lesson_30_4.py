"""Reference kernel for 30.4. Not a complete engine subsystem."""
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

MAXIMA={'gameplay':20,'systems':20,'correctness':20,'production':15,'performance':10,'documentation':10,'oral':5}
CHECKS={'clean_launch','save_recovery','critical_defects_resolved','independent_loop','live_change','network_demo'}
def solve(payload: dict) -> dict:
    scores,checks=payload['scores'],payload['checks']
    if not isinstance(scores,dict) or set(scores)!=set(MAXIMA) or not isinstance(checks,dict) or set(checks)!=CHECKS:
        raise ValueError('rubric schema')
    for name,maximum in MAXIMA.items():
        value=integer(scores[name])
        if value>maximum:raise ValueError('score exceeds category')
    if any(type(v)is not bool for v in checks.values()):raise ValueError('boolean check required')
    total=sum(scores.values()); blockers=sorted(k for k,v in checks.items() if not v)
    if total<80:blockers.append('score_below_80')
    return {'score':total,'passed':not blockers,'blockers':blockers}
