from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from python.reference.lab_19_2 import parse_request,canonical_request
raw=b'{"version":1,"id":"job-1","operation":"sum_squares","values":[2,3]}'
print(canonical_request(parse_request(raw)))
try:
    parse_request(raw.replace(b'[2,3]',b'[true,3]'))
except ValueError:
    print("boolean value rejected")
