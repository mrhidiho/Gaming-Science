from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
requirements={"REQ-1":"reject oversized frame","REQ-2":"drain accepted work","REQ-3":"deduplicate durable result"}
evidence={"REQ-1":["test_oversize"],"REQ-2":[],"REQ-3":["test_replay"]}
missing=[r for r in requirements if not evidence.get(r)]
print("Requirements missing evidence:",missing)
print("Named tests still need to be run and reviewed; names are not proof.")
