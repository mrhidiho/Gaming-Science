"""Runnable reference demonstration for lesson 30.2."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_30_2.py"
spec = importlib.util.spec_from_file_location("demo_lesson_30_2", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'text': 'Hi {name}', 'bindings': {'interact': 'Space'}, 'action': 'interact'}
print("Lesson 30.2: Pseudo-localization and current binding prompt")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
