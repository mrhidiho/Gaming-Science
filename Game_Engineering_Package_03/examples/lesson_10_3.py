# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import convolve
print("full convolution:", convolve([1, 2, 3], [0.5, 0.5]))
print("impulse response:", convolve([1], [0.25, 0.5, 0.25]))
x = [1, 1, 1, 1]
print("causal same-length prefix:", convolve(x, [0.5, 0.5])[:len(x)])
