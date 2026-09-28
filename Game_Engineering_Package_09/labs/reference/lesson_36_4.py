"""Lesson 36.4 computational slice.

Choose the first diagnostic action from Boolean observations: over_limit, power_ok, reset_released, clock_ok, id_ok, framing_ok. Check safety first, then power, reset, clock, identity and framing. This is a simulated decision tree, not a device-specific physical procedure.
"""
from __future__ import annotations

def solve(case: dict) -> dict:
    keys=['over_limit','power_ok','reset_released','clock_ok','id_ok','framing_ok']
    if any(not isinstance(case[k],bool) for k in keys): raise ValueError('Boolean observations required')
    if case['over_limit']: return {'action':'STOP_AND_ISOLATE'}
    for key,action in [('power_ok','REVIEW_SUPPLY'),('reset_released','REVIEW_RESET'),
                       ('clock_ok','REVIEW_CLOCK'),('id_ok','REVIEW_ID_PATH'),
                       ('framing_ok','REVIEW_PROTOCOL')]:
        if not case[key]: return {'action':action}
    return {'action':'RUN_BOUNDED_SELF_TEST'}
