"""Lesson 36.3 computational slice.

Lint a deliberately small board-review record, not a KiCad file. Required fields: supply_v, min_v, max_v, load_ma, budget_ma, footprint_verified and return_path_continuous. Report sorted issues. Even an empty list means only ready for qualified review, never authorization to fabricate or power hardware.
"""
from __future__ import annotations

from labs.common import number

def solve(case: dict) -> dict:
    for key in ['supply_v','min_v','max_v','load_ma','budget_ma']:
        number(case[key],key,minimum=0)
    if case['min_v']>case['max_v']: raise ValueError('inverted supply range')
    for key in ['footprint_verified','return_path_continuous']:
        if not isinstance(case[key],bool): raise ValueError('review flags must be Boolean')
    issues=[]
    if not case['min_v']<=case['supply_v']<=case['max_v']: issues.append('voltage')
    if case['load_ma']>case['budget_ma']: issues.append('current_budget')
    if not case['footprint_verified']: issues.append('footprint')
    if not case['return_path_continuous']: issues.append('return_path')
    return {'issues':sorted(issues),'ready_for_review':not issues}
