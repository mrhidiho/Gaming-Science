"""Lesson 30.4: Evidence-gate rubric evaluator.

Input scores with exactly gameplay,systems,correctness,production,performance,documentation,oral; maxima 20,20,20,15,10,10,5. checks with exactly clean_launch,save_recovery,critical_defects_resolved,independent_loop,live_change,network_demo (boolean). Return score,passed,blockers. Pass requires score>=80 and all checks true. This evaluates supplied claims only; it cannot verify human review or approve a capstone automatically.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 30.4; see LAB_WORKBOOK.pdf")
