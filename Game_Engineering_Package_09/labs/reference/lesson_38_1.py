"""Lesson 38.1 computational slice.

Return an Amdahl speedup and roofline bound. Inputs: unchanged_fraction in [0,1], acceleration >0, added_fraction >=0, compute_GFLOPs >0, bandwidth_GBs >0, intensity_FLOP_per_byte >=0. Added overhead is expressed as a fraction of ORIGINAL runtime. Decimal GB and GFLOP units cancel.
"""
from __future__ import annotations

from labs.common import number

def solve(case: dict) -> dict:
    s=number(case['unchanged_fraction'],'unchanged_fraction',minimum=0)
    if s>1: raise ValueError('fraction exceeds one')
    a=number(case['acceleration'],'acceleration',positive=True)
    h=number(case['added_fraction'],'added_fraction',minimum=0)
    peak=number(case['compute_GFLOPs'],'compute_GFLOPs',positive=True)
    bw=number(case['bandwidth_GBs'],'bandwidth_GBs',positive=True)
    intensity=number(case['intensity_FLOP_per_byte'],'intensity',minimum=0)
    return {'speedup':1/(s+(1-s)/a+h),'roof_GFLOPs':min(peak,bw*intensity)}
