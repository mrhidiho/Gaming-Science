"""Lesson 38.3 computational slice.

Model job placement. costs are nonnegative service times, workers is 1..256, overhead is per-job service cost. policy is round_robin or greedy (earliest available worker, ties lowest index). All jobs are ready at t=0. This does not simulate NUMA, work stealing, real threads or vector instructions.
"""
from __future__ import annotations

from labs.common import number, integer

def solve(case: dict) -> dict:
    workers=integer(case['workers'],'workers',1,256)
    overhead=number(case['overhead'],'overhead',minimum=0)
    policy=case['policy']
    if policy not in ['round_robin','greedy']: raise ValueError('unsupported policy')
    loads=[0.0]*workers
    for i,cost in enumerate(case['costs']):
        number(cost,'cost',minimum=0)
        target=i%workers if policy=='round_robin' else min(range(workers),key=lambda w:(loads[w],w))
        loads[target]+=cost+overhead
    return {'loads':loads,'makespan':max(loads),'total_service':sum(loads)}
