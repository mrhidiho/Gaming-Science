from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import os
from python.reference.lab_17_1 import run_child
r=run_child([2,3,5])
print("sum=",r["sum"]," separate_process=",r["pid"] != os.getpid(),sep="")
