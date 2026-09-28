"""Lesson 39.2 computational slice.

Simulate persistent progress independently of volatile graphics resources. Start RUNNING at tick 0, resource generation 1. Events: step, checkpoint, suspend, resume, kill, launch. suspend checkpoints in this educational contract; sudden kill does not. kill discards uncheckpointed progress. Resuming rebuilds resources with a new generation. Unsupported transitions raise ValueError.
"""
from __future__ import annotations

def solve(case: dict) -> dict:
    state='RUNNING'; tick=0; saved=0; generation=1; live=True
    for event in case['events']:
        if event=='step' and state=='RUNNING': tick+=1
        elif event=='checkpoint' and state=='RUNNING': saved=tick
        elif event=='suspend' and state=='RUNNING': saved=tick; state='SUSPENDED'; live=False
        elif event=='resume' and state=='SUSPENDED': state='RUNNING'; live=True; generation+=1
        elif event=='kill' and state!='KILLED': state='KILLED'; tick=saved; live=False
        elif event=='launch' and state=='KILLED': state='RUNNING'; tick=saved; live=True; generation+=1
        else: raise ValueError('unsupported lifecycle transition: '+event)
    return {'state':state,'tick':tick,'saved_tick':saved,'resources_live':live,'generation':generation}
