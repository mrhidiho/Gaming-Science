"""Lesson 29.3: Rollback to the pre-tick state.

Input integer initial, inputs list of integer deltas -1,0,1, corrections list [tick,delta], and oldest retained pre-tick index. Maximum 10000 inputs. Build predicted history, restore earliest corrected S_tick, replay through end, return states including S_0. Reject corrections older than oldest or outside tape, and conflicting duplicates. This bounded scalar model does not snapshot a full physics engine.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 29.3; see LAB_WORKBOOK.pdf")
