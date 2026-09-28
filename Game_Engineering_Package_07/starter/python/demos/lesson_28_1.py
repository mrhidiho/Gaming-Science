"""Runnable reference demonstration for lesson 28.1."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_28_1.py"
spec = importlib.util.spec_from_file_location("demo_lesson_28_1", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'grid': ['...'], 'start': [0, 0], 'goal': [2, 0], 'budget': 10}
print("Lesson 28.1: Budgeted four-connected A-star")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
