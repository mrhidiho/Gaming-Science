"""Lesson 37.3 computational slice.

Compute a resource-service lower bound with ideal overlap and a serial service estimate. demands and rates are dictionaries with identical nonempty resource keys; setup_s is nonnegative. All rates must be positive. Neither result is a hardware timing guarantee: queuing and dependencies are omitted.
"""
from __future__ import annotations

from labs.common import number

def solve(case: dict) -> dict:
    demands=case['demands']; rates=case['rates']; setup=number(case['setup_s'],'setup_s',minimum=0)
    if not demands or set(demands)!=set(rates): raise ValueError('matching resources required')
    times={k:number(v,k,minimum=0)/number(rates[k],k+' rate',positive=True) for k,v in demands.items()}
    return {'lower_s':setup+max(times.values()),'serial_s':setup+sum(times.values()),
            'dominant':min(k for k,v in times.items() if v==max(times.values()))}
