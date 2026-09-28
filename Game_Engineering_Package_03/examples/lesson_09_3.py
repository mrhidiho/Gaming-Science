# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import percentile, mean_interval
frames = [5.0]*19 + [100.0]  # synthetic, not a measured machine
print(f"synthetic mean: {sum(frames)/len(frames):.3f} ms")
print("nearest-rank p95 and p99:", percentile(frames, 0.95), percentile(frames, 0.99))
# Five illustrative independent normal run differences; B minus A in ms.
mean, low, high = mean_interval([1, 2, 3, 4, 5], 2.776445)
print(f"paired mean and illustrative t interval: {mean:.3f} [{low:.3f}, {high:.3f}]")
