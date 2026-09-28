"""Runnable reference demonstration for lesson 26.2."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_26_2.py"
spec = importlib.util.spec_from_file_location("demo_lesson_26_2", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'va': 3, 'vb': 0, 'wa': 0.5, 'wb': 0.5, 'e': 0.5}
print("Lesson 26.2: One-dimensional collision impulse")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
