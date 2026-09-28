"""Runnable reference demonstration for lesson 26.4."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_26_4.py"
spec = importlib.util.spec_from_file_location("demo_lesson_26_4", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'left': [{'x': 0, 'v': 1}, {'x': 1}], 'right': [{'v': 1, 'x': 0}, {'x': 2}]}
print("Lesson 26.4: Canonical replay and first divergence")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
