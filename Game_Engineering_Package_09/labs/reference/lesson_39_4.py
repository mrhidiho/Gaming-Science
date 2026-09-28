"""Lesson 39.4 computational slice.

Negotiate required and optional capabilities without guessing vendor access. supported, required and optional are lists of strings. Return sorted missing requirements and enabled optional capabilities. A backend is accepted only if every required capability is advertised. This structural check does not certify a platform.
"""
from __future__ import annotations

def solve(case: dict) -> dict:
    for key in ['supported','required','optional']:
        if not isinstance(case[key],list) or any(not isinstance(s,str) or not s for s in case[key]):
            raise ValueError('capabilities must be nonempty strings')
    supported=set(case['supported']); missing=set(case['required'])-supported
    return {'accepted':not missing,'missing':sorted(missing),
            'enabled_optional':sorted(set(case['optional']) & supported)}
