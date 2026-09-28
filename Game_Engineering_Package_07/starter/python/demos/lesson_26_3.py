"""Runnable reference demonstration for lesson 26.3."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_26_3.py"
spec = importlib.util.spec_from_file_location("demo_lesson_26_3", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'x': 0, 'v': 30, 'lo': 0.24, 'hi': 0.26, 'dt': 0.016666666666666666}
print("Lesson 26.3: Swept point versus one-dimensional slab")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
