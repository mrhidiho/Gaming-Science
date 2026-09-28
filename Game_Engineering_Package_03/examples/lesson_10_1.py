# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import gradient
f = lambda p: p[0]**2 + 3*p[1]**2
point = (2.0, -1.0)
g = gradient(f, point, 0.0001)
print("numerical gradient:", tuple(round(x, 6) for x in g))
print("analytic gradient:", (2*point[0], 6*point[1]))
alpha = 0.1
new = tuple(x-alpha*dx for x, dx in zip(point, g))
print(f"objective: {f(point):.3f} -> {f(new):.3f}")
