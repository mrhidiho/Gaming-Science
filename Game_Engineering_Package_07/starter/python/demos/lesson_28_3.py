"""Runnable reference demonstration for lesson 28.3."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_28_3.py"
spec = importlib.util.spec_from_file_location("demo_lesson_28_3", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'tree': [[3, 5], [2, 100]], 'budget': 100}
print("Lesson 28.3: Node-bounded alpha-beta value search")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
