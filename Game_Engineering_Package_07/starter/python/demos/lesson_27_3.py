"""Runnable reference demonstration for lesson 27.3."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_27_3.py"
spec = importlib.util.spec_from_file_location("demo_lesson_27_3", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'sample_rate': 8, 'frames': 4, 'frequencies': [1], 'gains': [0.5]}
print("Lesson 27.3: Offline phase-continuous tone mixer")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
