"""Runnable reference demonstration for lesson 29.1."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_29_1.py"
spec = importlib.util.spec_from_file_location("demo_lesson_29_1", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'position': 10, 'ack': 40, 'pending': [[44, 1], [40, 1], [41, 1], [43, 1], [42, 1]]}
print("Lesson 29.1: Input acknowledgment and reconciliation")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
