"""Lesson 38.4 computational slice.

Integrate interval-average power. times_s has one more item than power_w and completed_frames, and is strictly increasing. Each power value describes the entire following interval, not an instantaneous sample. Return energy, duration, average power and completed frames per joule; zero energy yields null efficiency.
"""
from __future__ import annotations

from labs.common import number, integer

def solve(case: dict) -> dict:
    times=case['times_s']; powers=case['power_w']; frames=case['completed_frames']
    if len(times)<2 or len(times)!=len(powers)+1 or len(powers)!=len(frames): raise ValueError('interval array mismatch')
    for t in times: number(t,'time_s',minimum=0)
    energy=0.0
    for i,p in enumerate(powers):
        number(p,'power_w',minimum=0); integer(frames[i],'frames')
        dt=times[i+1]-times[i]
        if dt<=0: raise ValueError('times must increase')
        energy+=p*dt
    duration=times[-1]-times[0]
    return {'joules':energy,'duration_s':duration,'average_w':energy/duration,
            'frames_per_joule':sum(frames)/energy if energy else None}
