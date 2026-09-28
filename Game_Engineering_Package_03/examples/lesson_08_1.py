# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import centered_difference
f = lambda t: t ** 3
x = 2.0
exact = 3 * x * x
for h in (0.1, 0.01, 0.001):
    estimate = centered_difference(f, x, h)
    print(f"h={h:.3f} estimate={estimate:.6f} error={abs(estimate-exact):.6f}")
