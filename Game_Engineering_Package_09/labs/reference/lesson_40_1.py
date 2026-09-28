"""Lesson 40.1 computational slice.

Calculate a bounded additive-frame proposal. frame_ms >0; 0<= operation_ms <= frame_ms; acceleration >0; overhead_ms >=0. maximum_saved_fraction assumes the operation disappears with zero overhead. New frame time uses the supplied finite acceleration. An overlapped operation off the critical path cannot use this model without justification.
"""
from __future__ import annotations

from labs.common import number

def solve(case: dict) -> dict:
    frame=number(case['frame_ms'],'frame_ms',positive=True)
    operation=number(case['operation_ms'],'operation_ms',minimum=0)
    if operation>frame: raise ValueError('operation exceeds additive frame')
    acceleration=number(case['acceleration'],'acceleration',positive=True)
    overhead=number(case['overhead_ms'],'overhead_ms',minimum=0)
    new=frame-operation+operation/acceleration+overhead
    return {'maximum_saved_fraction':operation/frame,'new_frame_ms':new,'application_speedup':frame/new}
