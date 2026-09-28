# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import math
from mathkit import translation, rotation_z, matmul, transform4, quat_rotate
parent = matmul(translation(10, 0, 0), rotation_z(math.pi / 2))
child = translation(2, 0, 0)
world = matmul(parent, child)
print("child origin:", tuple(round(x, 6) for x in transform4(world, (0, 0, 0, 1))))
print("direction:", transform4(translation(10, 20, 30), (1, 0, 0, 0)))
q = (math.cos(math.pi / 4), 0, 0, math.sin(math.pi / 4))
print("quaternion:", tuple(round(x, 6) for x in quat_rotate(q, (1, 0, 0))))
