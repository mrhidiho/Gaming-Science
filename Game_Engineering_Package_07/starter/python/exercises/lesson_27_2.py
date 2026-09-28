"""Lesson 27.2: Analytic two-link inverse kinematics.

Input positive lengths l1,l2 and finite target x,y. Return shoulder, elbow, endpoint and reachable flag. Choose nonnegative elbow angle. Clamp target radius to [abs(l1-l2),l1+l2]; at zero target direction use +x. Equality is reachable; no joint-angle limits or 3D model.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 27.2; see LAB_WORKBOOK.pdf")
