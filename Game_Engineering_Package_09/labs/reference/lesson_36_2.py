"""Lesson 36.2 computational slice.

Simulate integer-tick, single-core, preemptive fixed-priority periodic tasks. Each task has name, period, cost, deadline and priority (lower wins). All first releases occur at tick 0. horizon is 1..10000; deadlines are relative and <= period. Deadline misses count unfinished jobs when their deadline occurs, not merely at horizon.
"""
from __future__ import annotations

from labs.common import integer

def solve(case: dict) -> dict:
    horizon=integer(case['horizon'],'horizon',1,10000)
    tasks=case['tasks']; names=set()
    for task in tasks:
        if task['name'] in names: raise ValueError('duplicate task name')
        names.add(task['name'])
        period=integer(task['period'],'period',1)
        integer(task['cost'],'cost',1)
        integer(task['deadline'],'deadline',1,period)
        integer(task['priority'],'priority')
    jobs=[]; completed=0; missed=0; released=0
    for t in range(horizon):
        for index,task in enumerate(tasks):
            if t % task['period']==0:
                jobs.append({'remaining':task['cost'],'deadline':t+task['deadline'],
                             'priority':task['priority'],'release':t,'index':index,'missed':False})
                released+=1
        ready=[j for j in jobs if j['remaining']]
        if ready:
            job=min(ready,key=lambda j:(j['priority'],j['release'],j['index']))
            job['remaining']-=1
            if job['remaining']==0: completed+=1
        for job in jobs:
            if job['deadline']==t+1 and job['remaining'] and not job['missed']:
                job['missed']=True; missed+=1
    return {'released':released,'completed':completed,'missed':missed,
            'pending':sum(j['remaining']>0 for j in jobs)}
