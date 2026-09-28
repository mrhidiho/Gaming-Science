"""Ideal analytical circuit and sampled-input models. These are NOT SPICE results."""
from dataclasses import dataclass
import math
from typing import Optional

def positive(*values: float) -> None:
    if any(not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError("parameters must be finite and positive")

@dataclass(frozen=True)
class DividerResult:
    voltage: float
    source_current: float
    bottom_current: float
    load_current: float
    kcl_residual: float
    source_power: float
    resistor_power: float

def divider(vs: float, r1: float, r2: float, load: Optional[float] = None) -> DividerResult:
    positive(r1, r2)
    if not math.isfinite(vs):
        raise ValueError("source voltage must be finite")
    if load is not None:
        positive(load)
    rb = r2 if load is None else 1.0 / (1.0 / r2 + 1.0 / load)
    v = vs * rb / (r1 + rb)
    it = (vs - v) / r1
    ib = v / r2
    il = 0.0 if load is None else v / load
    power = (vs-v)**2/r1 + v*v/r2 + (0.0 if load is None else v*v/load)
    return DividerResult(v, it, ib, il, it-ib-il, vs*it, power)

def divider_bounds(vs: float, r1: float, r2: float, tolerance: float) -> tuple[float, float]:
    positive(r1, r2)
    if not math.isfinite(vs) or vs < 0 or not 0 <= tolerance < 1:
        raise ValueError("requires nonnegative source and tolerance in [0,1)")
    lo = divider(vs,r1*(1+tolerance),r2*(1-tolerance)).voltage
    hi = divider(vs,r1*(1-tolerance),r2*(1+tolerance)).voltage
    return lo,hi

def rc_step(t: float, r: float, c: float, vs: float, initial: float = 0.0) -> float:
    positive(r,c)
    if not all(math.isfinite(x) for x in (t,vs,initial)) or t < 0:
        raise ValueError("finite values and t >= 0 required")
    return vs+(initial-vs)*math.exp(-t/(r*c))

def rc_response(frequency: float,r:float,c:float) -> tuple[float,float]:
    positive(r,c)
    if not math.isfinite(frequency) or frequency < 0:
        raise ValueError("frequency must be finite and nonnegative")
    x=2*math.pi*frequency*r*c
    return 1/math.sqrt(1+x*x),-math.atan(x)  # radians

def rc_euler(steps:int, dt:float,r:float,c:float,vs:float,initial:float=0.0) -> list[float]:
    positive(dt,r,c)
    if not isinstance(steps,int) or steps<0 or not all(math.isfinite(x) for x in (vs,initial)):
        raise ValueError("nonnegative integer steps and finite voltages required")
    result=[initial]
    for _ in range(steps):
        result.append(result[-1]+dt/(r*c)*(vs-result[-1]))
    return result  # intentionally allows unstable dt: lesson studies it

class Hysteresis:
    def __init__(self,low:float=1.5,high:float=1.8,initial:int=0):
        if not all(math.isfinite(x) for x in (low,high)) or low>=high or initial not in (0,1):
            raise ValueError("low < high and binary initial state required")
        self.low,self.high,self.state=low,high,initial
    def update(self,value:float) -> int:
        if not math.isfinite(value): raise ValueError("finite sample required")
        if value>=self.high: self.state=1
        elif value<=self.low: self.state=0
        return self.state

def quantize(voltage:float,bits:int=12,vref:float=3.3) -> int:
    positive(vref)
    if not isinstance(bits,int) or not 1<=bits<=32 or not math.isfinite(voltage):
        raise ValueError("bits must be 1..32; voltage finite")
    levels=1<<bits
    if voltage<=0:return 0
    if voltage>=vref:return levels-1
    return math.floor(voltage/vref*levels)

def reconstruct(code:int,bits:int=12,vref:float=3.3) -> float:
    positive(vref)
    if not isinstance(bits,int) or not 1<=bits<=32 or not isinstance(code,int) or not 0<=code<(1<<bits):
        raise ValueError("code outside quantizer range")
    return (code+0.5)*vref/(1<<bits)

def lowpass(samples:list[float],alpha:float,initial:float=0.0)->list[float]:
    if not math.isfinite(alpha) or not 0<alpha<=1 or not math.isfinite(initial):
        raise ValueError("alpha in (0,1] and finite initial state required")
    y=initial; result=[]
    for x in samples:
        if not math.isfinite(x): raise ValueError("finite samples required")
        y+=alpha*(x-y);result.append(y)
    return result

if __name__=='__main__':
    from dataclasses import asdict
    import json
    print(json.dumps({'model':'ideal analytical; not SPICE',
        'loaded_divider':asdict(divider(5,2000,3000,6000)),
        'one_percent_bounds':divider_bounds(5,2000,3000,.01),
        'rc_one_tau':rc_step(.01,10000,1e-6,3.3)},indent=2))
