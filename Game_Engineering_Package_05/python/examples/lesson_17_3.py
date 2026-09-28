from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from python.reference.lab_17_3 import schedule_fcfs
for row in schedule_fcfs([(0,12,100),(1,1,5)]):
    print(row)
print("Times above are model units, not measured OS latency.")
