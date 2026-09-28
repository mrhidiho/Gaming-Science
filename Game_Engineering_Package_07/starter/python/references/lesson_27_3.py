"""Reference kernel for 27.3. Not a complete engine subsystem."""
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
    sr=finite(payload['sample_rate']); n=integer(payload['frames'])
    freqs=[finite(v) for v in payload['frequencies']]; gains=[finite(v) for v in payload['gains']]
    phases=[finite(v) for v in payload.get('phases',[0.0]*len(freqs))]
    if sr<=0 or n>65536 or not 1<=len(freqs)<=8 or len(gains)!=len(freqs) or len(phases)!=len(freqs):
        raise ValueError('format or voice count')
    if any(not 0<f<sr/2 for f in freqs) or sum(abs(g) for g in gains)>1+1e-12:
        raise ValueError('frequency/gain domain')
    increments=[math.tau*f/sr for f in freqs]; out=[]
    phases=[p%math.tau for p in phases]
    for _ in range(n):
        out.append(sum(g*math.sin(p) for g,p in zip(gains,phases)))
        phases=[(p+d)%math.tau for p,d in zip(phases,increments)]
    return {'samples':out,'phases':phases}
