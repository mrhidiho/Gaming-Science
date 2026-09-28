"""Runnable reference demonstration for lesson 30.1."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_30_1.py"
spec = importlib.util.spec_from_file_location("demo_lesson_30_1", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'times_ms': [10, 10, 10, 10, 50], 'budget_ms': 16.67}
print("Lesson 30.1: Nearest-rank frame statistics")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
