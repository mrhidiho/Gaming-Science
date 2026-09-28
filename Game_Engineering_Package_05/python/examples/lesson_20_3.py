from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import hashlib
source=ROOT/"native"/"worker.cpp"
before=hashlib.sha256(source.read_bytes()).hexdigest()
changed=hashlib.sha256(source.read_bytes()+b"\n").hexdigest()
print("change detected=",before!=changed,sep="")
print("A digest detects byte changes against a trusted value; it is not authentication.")
