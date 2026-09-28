"""Runnable reference demonstration for lesson 28.4."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_28_4.py"
spec = importlib.util.spec_from_file_location("demo_lesson_28_4", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'x': [1, 2], 'w': [0, 0], 'b': 0, 'y': 1, 'lr': 0.1}
print("Lesson 28.4: One stable logistic gradient step")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
