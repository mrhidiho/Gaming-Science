from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import tempfile
from python.reference.lab_17_4 import write_save,read_save,InjectedFailure
with tempfile.TemporaryDirectory() as d:
    path=Path(d)/"save.json"
    write_save(path,{"version":1,"score":7})
    try:
        write_save(path,{"version":1,"score":99},"partial_write")
    except InjectedFailure:
        print("injected failure; old score=",read_save(path)["score"],sep="")
    write_save(path,{"version":1,"score":99})
    print("new score=",read_save(path)["score"],sep="")
