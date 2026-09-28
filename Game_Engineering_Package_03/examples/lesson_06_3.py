# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import count_positive_prefix
health = [4, 0, -1, 9]
for k in range(len(health) + 1):
    print(f"prefix {k}: {count_positive_prefix(health, k)} living")
n = 100
print("sum and formula:", sum(range(n + 1)), n * (n + 1) // 2)
