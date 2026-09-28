# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import dot, normalize
v = (3, 4)
u = normalize(v)
print("unit:", tuple(round(x, 3) for x in u))
print("x component:", dot(v, (1, 0)))
print("squared length:", dot(v, v))
try:
    normalize((0, 0))
except ValueError as error:
    print("rejected:", error)
