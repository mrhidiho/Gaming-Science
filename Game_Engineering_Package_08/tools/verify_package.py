"""Verify release checksums. Running labs later may intentionally change evidence."""
import hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
failures=[];checked=0
for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
    digest,name=line.split('  ',1);path=(ROOT/name).resolve()
    if ROOT not in path.parents:
        failures.append(name+': invalid path');continue
    if not path.is_file():failures.append(name+': missing');continue
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    checked+=1
    if h.hexdigest()!=digest:failures.append(name+': changed')
print(f'Checked {checked} release files; mismatches={len(failures)}')
for failure in failures:print(failure)
sys.exit(1 if failures else 0)
