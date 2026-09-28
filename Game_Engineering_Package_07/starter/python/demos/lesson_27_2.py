"""Runnable reference demonstration for lesson 27.2."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_27_2.py"
spec = importlib.util.spec_from_file_location("demo_lesson_27_2", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'l1': 1, 'l2': 1, 'x': 1, 'y': 1}
print("Lesson 27.2: Analytic two-link inverse kinematics")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
