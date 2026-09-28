"""Runnable reference demonstration for lesson 26.1."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_26_1.py"
spec = importlib.util.spec_from_file_location("demo_lesson_26_1", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'circles': [[2, -0.1, 0, 0.2], [1, 0.15, 0, 0.1]], 'cell_size': 1}
print("Lesson 26.1: Conservative grid and circle contacts")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
