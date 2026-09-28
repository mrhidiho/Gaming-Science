# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import descent_quadratic
for alpha in (0.25, 1.0, 1.1):
    result = descent_quadratic(0, alpha, max_steps=8, tol=0.03)
    print(f"alpha={alpha:.2f} x={result['x']:.6f} steps={result['iterations']} reason={result['reason']}")
