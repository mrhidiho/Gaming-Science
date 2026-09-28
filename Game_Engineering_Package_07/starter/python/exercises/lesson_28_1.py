"""Lesson 28.1: Budgeted four-connected A-star.

Input rectangular grid strings ('.' free, '#' blocked), start/goal [x,y], budget>=0. Maximum 128 by 128. Return status found/unreachable/budget_exhausted, path and expanded count. Unit moves, Manhattan heuristic, lexicographic heap tie-break. Blocked start/goal is unreachable. Goal removal counts as an expansion.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 28.1; see LAB_WORKBOOK.pdf")
