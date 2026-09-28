# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import constant_acceleration, spring_step
x, v = constant_acceleration(0, 4, -10, 0.5)
print(f"projectile: x={x:.3f} m, v={v:.3f} m/s")
x, v = spring_step(0.2, 0, 2, 50, 1, 0.01, "semi")
print(f"spring: x={x:.5f} m, v={v:.5f} m/s")
