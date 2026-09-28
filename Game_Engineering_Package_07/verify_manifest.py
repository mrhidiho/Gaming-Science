"""Verify files against MANIFEST.json. This checks integrity, not authenticity."""
from pathlib import Path
import hashlib
import json
import sys

def main():
    root=Path(__file__).resolve().parent
    try:manifest=json.loads((root/'MANIFEST.json').read_text())
    except (OSError,ValueError) as exc:print('Cannot read manifest:',exc);return 1
    failures=[]
    for item in manifest['files']:
        path=(root/item['path']).resolve()
        if not path.is_relative_to(root):failures.append(item['path']+': unsafe path');continue
        if not path.is_file():failures.append(item['path']+': missing');continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=item['sha256']:failures.append(item['path']+': changed')
    for line in failures:print('FAIL',line)
    print(f"{len(manifest['files'])-len(failures)} verified; {len(failures)} failed. Hash comparison is not publisher authentication.")
    return bool(failures)
if __name__=='__main__':sys.exit(main())
