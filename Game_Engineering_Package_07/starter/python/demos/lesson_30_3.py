"""Runnable reference demonstration for lesson 30.3."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_30_3.py"
spec = importlib.util.spec_from_file_location("demo_lesson_30_3", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'version': 1, 'title': 'Relay', 'textures': [{'name': 'icon', 'width': 64, 'height': 64}]}
print("Lesson 30.3: Bounded data-only mod schema")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
