# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import integrate
for n in (4, 8, 16):
    left = integrate(lambda t: t*t, 0, 1, n, "left")
    trap = integrate(lambda t: t*t, 0, 1, n, "trapezoid")
    print(f"n={n:2} left={left:.6f} trapezoid={trap:.6f}")
print("exact:", round(1/3, 6))
print("linear trapezoid:", integrate(lambda t: 2*t, 0, 3, 4))
