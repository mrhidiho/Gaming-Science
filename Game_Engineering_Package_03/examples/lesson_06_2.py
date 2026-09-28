# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import implies
for p in (False, True):
    for q in (False, True):
        print(f"{int(p)} -> {int(q)} = {int(implies(p, q))}")
health = [5, 0, 8]
print("all positive:", all(h > 0 for h in health))
print("counterexample indices:", [i for i, h in enumerate(health) if h <= 0])
