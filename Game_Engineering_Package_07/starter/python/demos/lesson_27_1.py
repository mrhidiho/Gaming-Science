"""Runnable reference demonstration for lesson 27.1."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_27_1.py"
spec = importlib.util.spec_from_file_location("demo_lesson_27_1", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'parents': [-1, 0], 'local': [[0, 0, 1.5707963267948966], [1, 0, 0]]}
print("Lesson 27.1: Parent-first two-dimensional pose evaluation")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
