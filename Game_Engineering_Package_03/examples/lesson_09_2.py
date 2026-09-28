# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import random
from mathkit import weighted_index
rng = random.Random(2026)
weights, rewards = (70, 25, 5), (0, 5, 20)
counts = [0, 0, 0]
for _ in range(1000):
    counts[weighted_index(weights, rng.random())] += 1
print("seed: 2026; trials: 1000")
print("counts:", counts)
expected = sum(w*r for w, r in zip(weights, rewards))/sum(weights)
print(f"model expectation: {expected:.3f}")
print(f"sample mean: {sum(c*r for c,r in zip(counts,rewards))/1000:.3f}")
