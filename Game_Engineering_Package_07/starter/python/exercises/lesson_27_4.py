"""Lesson 27.4: Equal-power pan and stable presentation events.

Input pan in [-1,1], seen/events lists of [epoch_string,tick,entity,index], and min_tick>=0. Return gains [left,right], emitted unique events in arrival order, and retained identities sorted. Ignore events older than min_tick. Inputs at most 4096 identities each; retained union cap 8192. Epoch is part of identity. Full runtime must prune by its rollback horizon.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 27.4; see LAB_WORKBOOK.pdf")
