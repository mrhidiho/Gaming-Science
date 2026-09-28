"""Lesson 42.2: Tiling, data reuse and asynchronous pipelines

Warm-up contract
Model a perfect two-stage pipeline with one copy engine and one compute engine, two buffers, fixed stage costs and no contention. For n>0 return copy+compute+(n-1)*max(copy,compute); for n=0 return 0. This is an analytical model, not a timer.

Implement this yourself before reading reference code. Add your own edge tests.
The full lab and two graduate problems are in LAB_WORKBOOK.pdf.
Passing this warm-up does NOT satisfy the full lesson or project.
"""
from __future__ import annotations


def solve(case: dict):
    """Return the value specified above; validate inputs used by your contract."""
    raise NotImplementedError("Implement lesson 42.2 warm-up")
