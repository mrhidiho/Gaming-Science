from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import random
from python.reference.lab_19_2 import parse_request
rng=random.Random(2026);rejected=0
for _ in range(500):
    raw=bytes(rng.randrange(256) for _ in range(rng.randrange(129)))
    try:
        parse_request(raw)
    except ValueError:
        rejected+=1
print("bounded random inputs=500 rejected=",rejected,sep="")
print("No observed unexpected exception; not a security proof.")
