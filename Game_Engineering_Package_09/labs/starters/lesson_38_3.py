"""Lesson 38.3 computational slice.

Model job placement. costs are nonnegative service times, workers is 1..256, overhead is per-job service cost. policy is round_robin or greedy (earliest available worker, ties lowest index). All jobs are ready at t=0. This does not simulate NUMA, work stealing, real threads or vector instructions.
"""
from __future__ import annotations


def solve(case: dict) -> dict:
    """Implement the documented contract; do not import the reference solution."""
    raise NotImplementedError("Implement lesson 38.3")
