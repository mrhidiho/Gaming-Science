"""Educational globally-stalling register pipeline, not a cycle-accurate GPU/FPGA.

Each packet contains at most `lanes` scalar values. Arithmetic is evaluated on
acceptance; registers represent a declared latency, not synthesis evidence.
Output backpressure freezes all occupied stages and prevents a new acceptance.
First acceptance is edge 0; a latency-L packet can retire on edge L. The elapsed
cycle metric is last_retire_edge - first_accept_edge, not the count of sampled
edges. The model has no internal memory-port, clock-domain or routing effects.
"""
from __future__ import annotations
from collections.abc import Sequence
from labs.common import integer
from labs.reference.lesson_40_2 import solve as affine


def _packet_arithmetic(packet: Sequence[int], gain: int, bias: int) -> list[int]:
    """Independent magnitude-based Q8.8 implementation for the modeled datapath.

    The lesson oracle uses floor quotient/remainder on signed values. This path
    rounds the nonnegative magnitude first, then restores sign. All arguments
    are validated against the signed-16 contract before packet acceptance.
    """
    result=[]
    for value in packet:
        product=value*gain
        magnitude=abs(product)
        quotient=magnitude//256
        remainder=magnitude%256
        if remainder>128 or (remainder==128 and quotient%2): quotient+=1
        rounded=-quotient if product<0 else quotient
        result.append(max(-32768,min(32767,rounded+bias)))
    return result


def simulate(values: Sequence[int], *, lanes: int=1, latency: int=4,
             ready_pattern: Sequence[bool]=(True,), gain: int=384,
             bias: int=64, max_ticks: int=1_000_000) -> dict:
    integer(lanes,'lanes',1,64); integer(latency,'latency',1,256)
    integer(max_ticks,'max_ticks',1)
    if not ready_pattern or any(type(x) is not bool for x in ready_pattern):
        raise ValueError('ready_pattern must contain Booleans')
    if not any(ready_pattern): raise ValueError('output can never become ready')
    # Validate all arithmetic inputs even for runs that might time out.
    expected=affine(dict(bits=16,frac=8,gain=gain,bias=bias,x=list(values)))['raw']
    if not values:
        return dict(output=[],elapsed_cycles=0,tick_count=0,stalled_ticks=0,
                    accepted_packets=0,retired_packets=0,trace=[])
    packets=[list(values[i:i+lanes]) for i in range(0,len(values),lanes)]
    stages=[None]*latency; cursor=0; result=[]; trace=[]; stalled=0; retired=0
    first_accept=None; last_retire=None
    for tick in range(max_ticks):
        ready=ready_pattern[tick % len(ready_pattern)]
        retiring=stages[-1] is not None and ready
        can_advance=stages[-1] is None or ready
        if retiring:
            result.extend(stages[-1]); retired+=1; last_retire=tick
        accepted=False
        if can_advance:
            for j in range(latency-1,0,-1): stages[j]=stages[j-1]
            if cursor<len(packets):
                stages[0]=_packet_arithmetic(packets[cursor],gain,bias)
                cursor+=1; accepted=True
                if first_accept is None: first_accept=tick
            else: stages[0]=None
        else: stalled+=1
        if len(trace)<128:
            trace.append(dict(edge=tick,ready=ready,accepted=accepted,retired=retiring,
                              occupancy=sum(s is not None for s in stages)))
        if cursor==len(packets) and all(stage is None for stage in stages):
            if result!=expected: raise AssertionError('pipeline diverged from reference')
            return dict(output=result,elapsed_cycles=last_retire-first_accept,
                        tick_count=tick+1,stalled_ticks=stalled,accepted_packets=cursor,
                        retired_packets=retired,trace=trace)
    raise TimeoutError('bounded model did not drain; no completion claim is made')
