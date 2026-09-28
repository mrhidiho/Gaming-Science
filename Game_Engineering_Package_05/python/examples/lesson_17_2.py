from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import tempfile
from python.reference.lab_17_2 import file_digests
with tempfile.TemporaryDirectory() as d:
    path=Path(d)/"asset.bin"
    path.write_bytes(bytes(range(256))*16)
    a,b=file_digests(path)
    print("equal=",a==b," bytes=",path.stat().st_size,sep="")
