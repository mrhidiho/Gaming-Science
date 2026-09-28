"""Runnable reference demonstration for lesson 30.4."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_30_4.py"
spec = importlib.util.spec_from_file_location("demo_lesson_30_4", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'scores': {'gameplay': 20, 'systems': 20, 'correctness': 20, 'production': 15, 'performance': 10, 'documentation': 10, 'oral': 5}, 'checks': {'clean_launch': True, 'save_recovery': True, 'critical_defects_resolved': True, 'independent_loop': True, 'live_change': True, 'network_demo': True}}
print("Lesson 30.4: Evidence-gate rubric evaluator")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
