"""Runnable reference demonstration for lesson 29.2."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_29_2.py"
spec = importlib.util.spec_from_file_location("demo_lesson_29_2", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'snapshots': [[1.1, 4], [1, 2]], 'time': 1.04}
print("Lesson 29.2: Timestamped snapshot interpolation")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
