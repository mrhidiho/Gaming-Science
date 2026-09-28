"""Runnable reference demonstration for lesson 29.3."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_29_3.py"
spec = importlib.util.spec_from_file_location("demo_lesson_29_3", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'initial': 0, 'inputs': [1, 1, 0, 1], 'corrections': [[2, -1]], 'oldest': 0}
print("Lesson 29.3: Rollback to the pre-tick state")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
