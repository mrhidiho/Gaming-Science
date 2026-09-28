# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import spring_step
for method in ("explicit", "semi"):
    x, v = 1.0, 0.0
    for _ in range(20):
        x, v = spring_step(x, v, 1, 100, 0, 0.05, method)
    energy = 0.5*v*v + 50*x*x
    print(f"{method}: E/E0={energy/50:.6f}")
print(f"explicit prediction: {(1 + 100*0.05**2)**20:.6f}")
