"""Lesson 39.1 computational slice.

Summarize a synthetic one-clock input/presentation trace. input_ms and present_ms are same-length lists with at least two rows; presentation is strictly increasing and never precedes its corresponding input. timestamp_kind must equal synthetic_present. Return mean/p95 input-to-modeled-present and presentation-interval extrema. No photon measurement is inferred.
"""
from __future__ import annotations

import statistics
from labs.common import number, nearest_rank

def solve(case: dict) -> dict:
    ins=case['input_ms']; pres=case['present_ms']
    if case['timestamp_kind']!='synthetic_present': raise ValueError('unsupported timestamp boundary')
    if len(ins)<2 or len(ins)!=len(pres): raise ValueError('matching traces required')
    for value in ins+pres: number(value,'timestamp',minimum=0)
    if any(p<i for i,p in zip(ins,pres)): raise ValueError('negative latency')
    intervals=[b-a for a,b in zip(pres,pres[1:])]
    if any(t<=0 for t in intervals): raise ValueError('presentation must increase')
    latencies=[p-i for i,p in zip(ins,pres)]
    return {'mean_latency_ms':statistics.mean(latencies),'p95_latency_ms':nearest_rank(latencies,.95),
            'min_interval_ms':min(intervals),'max_interval_ms':max(intervals),
            'mean_rate_fps':1000/statistics.mean(intervals),'boundary':'synthetic_present'}
