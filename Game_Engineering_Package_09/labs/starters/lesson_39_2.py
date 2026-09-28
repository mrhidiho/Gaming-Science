"""Lesson 39.2 computational slice.

Simulate persistent progress independently of volatile graphics resources. Start RUNNING at tick 0, resource generation 1. Events: step, checkpoint, suspend, resume, kill, launch. suspend checkpoints in this educational contract; sudden kill does not. kill discards uncheckpointed progress. Resuming rebuilds resources with a new generation. Unsupported transitions raise ValueError.
"""
from __future__ import annotations


def solve(case: dict) -> dict:
    """Implement the documented contract; do not import the reference solution."""
    raise NotImplementedError("Implement lesson 39.2")
