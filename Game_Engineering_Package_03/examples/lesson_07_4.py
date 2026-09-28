# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import fit_line
xs = (0, 1, 2, 3, 4)
ys = (1.1, 2.9, 5.2, 6.8, 9.0)
slope, intercept = fit_line(xs, ys)
print(f"line: y = {slope:.3f} x + {intercept:.3f}")
print("residuals:", [round(y - (slope*x + intercept), 3) for x, y in zip(xs, ys)])
x, y = 1.0, 1.0
for _ in range(4):
    x, y = 2*x, 0.5*y
print("four diagonal updates:", (x, y))
