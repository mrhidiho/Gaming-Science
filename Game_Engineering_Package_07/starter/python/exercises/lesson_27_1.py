"""Lesson 27.1: Parent-first two-dimensional pose evaluation.

Input parents (root=-1) and local transforms [x,y,angle_radians], at most 256 joints. Return world transforms in original joint-index order. Imported order may be arbitrary. Reject cycles, invalid parents, non-finite transforms and mismatched counts. Column-vector parent*local convention; no scale/skinning in the kernel.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 27.1; see LAB_WORKBOOK.pdf")
