"""Runnable reference demonstration for lesson 27.4."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_27_4.py"
spec = importlib.util.spec_from_file_location("demo_lesson_27_4", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'pan': 0, 'seen': [['m', 90, 12, 0]], 'events': [['m', 90, 12, 0], ['m', 90, 12, 1]]}
print("Lesson 27.4: Equal-power pan and stable presentation events")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
