"""Lesson 37.1 computational slice.

Compute active-lane efficiency in an educational serialized-path group. paths is a nonempty list of A/B values of length <= width. Path costs and common cost are integer issue slots; at least one slot must execute. Count inactive tail lanes in capacity. This is not a cycle-accurate GPU model or an occupancy calculator.
"""
from __future__ import annotations

from labs.common import integer

def solve(case: dict) -> dict:
    width=integer(case['width'],'width',1)
    paths=case['paths']
    if not paths or len(paths)>width or any(p not in ['A','B'] for p in paths): raise ValueError('invalid paths')
    common=integer(case['common'],'common')
    a=integer(case['a_cost'],'a_cost'); b=integer(case['b_cost'],'b_cost')
    issued=common+(a if 'A' in paths else 0)+(b if 'B' in paths else 0)
    if issued==0: raise ValueError('zero issue slots')
    useful=len(paths)*common+sum(a if p=='A' else b for p in paths)
    return {'issued_slots':issued,'useful_lane_slots':useful,
            'efficiency':useful/(width*issued)}
