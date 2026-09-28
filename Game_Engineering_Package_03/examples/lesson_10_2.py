# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import math
from mathkit import alias_frequency
print("alias magnitude:", alias_frequency(900, 1000), "Hz")
# Cosines match; a 900 Hz sine would be the NEGATIVE of the 100 Hz sine.
errors = [abs(math.cos(2*math.pi*900*n/1000) - math.cos(2*math.pi*100*n/1000)) for n in range(10)]
print("cosine samples agree within 1e-12:", max(errors) < 1e-12)
checker = [0, 1]*4
print("raw decimation:", checker[::2])
print("pair-averaged decimation:", [(checker[i]+checker[i+1])/2 for i in range(0, len(checker), 2)])
