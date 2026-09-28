"""Runnable reference demonstration for lesson 29.4."""
from pathlib import Path
import importlib.util
import json

path = Path(__file__).resolve().parents[1] / "references" / "lesson_29_4.py"
spec = importlib.util.spec_from_file_location("demo_lesson_29_4", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = {'principal': 'match_authority', 'operation': {'id': 'R17', 'player': 'P', 'points': 50}, 'ledger': [], 'balances': {}}
print("Lesson 29.4: Idempotent result-store model")
print("INPUT:", json.dumps(payload, sort_keys=True))
print("OUTPUT:", json.dumps(module.solve(payload), indent=2, sort_keys=True))
