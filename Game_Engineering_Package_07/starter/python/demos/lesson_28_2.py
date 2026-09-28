"""Runnable reference demonstration for lesson 28.2."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_28_2.py"
spec = importlib.util.spec_from_file_location("demo_lesson_28_2", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'scores': {'attack': 0.64, 'retreat': 0.6}, 'current': 'retreat', 'margin': 0.05}
print("Lesson 28.2: Deterministic utility selection with hysteresis")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
