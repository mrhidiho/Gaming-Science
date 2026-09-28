"""Lesson 44.4: Formal specifications, replay and reliability-oriented engine design

Warm-up contract
Return the shortest bad event trace for the deliberately unguarded one-request lifecycle. Starting live and idle, a request is legal only while alive; complete requires pending work; release kills the owner. Enumerate histories rather than hard-coding the answer.

Implement this yourself before reading reference code. Add your own edge tests.
The full lab and two graduate problems are in LAB_WORKBOOK.pdf.
Passing this warm-up does NOT satisfy the full lesson or project.
"""
from __future__ import annotations


def solve(case: dict):
    """Return the value specified above; validate inputs used by your contract."""
    raise NotImplementedError("Implement lesson 44.4 warm-up")
