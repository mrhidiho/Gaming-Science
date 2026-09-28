# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import math
from mathkit import travel_time
print(f"travel time: {travel_time(36, 6):.1f} s")
angle = math.radians(90)
print(f"direction: ({math.cos(angle):.3f}, {math.sin(angle):.3f})")
print(f"halvings of 1024: {int(math.log2(1024))}")
