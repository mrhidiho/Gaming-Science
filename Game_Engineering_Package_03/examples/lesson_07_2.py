# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import matmul, solve2
rotation = ((0, -1), (1, 0))
scale = ((2, 0), (0, 1))
p = ((1,), (1,))
print("rotate then scale:", matmul(matmul(scale, rotation), p))
print("scale then rotate:", matmul(matmul(rotation, scale), p))
print("solve:", solve2(((2, 1), (1, -1)), (5, 1)))
