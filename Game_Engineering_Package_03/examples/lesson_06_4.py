# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import halving_steps, topological_order
graph = {"assets": ["scene"], "device": ["scene"], "scene": []}
print("order:", topological_order(graph))
print("loadouts:", 3 ** 4)
print("complete graph edges:", 5 * 4 // 2)
print("halving steps:", halving_steps(1024))
