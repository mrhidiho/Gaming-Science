#!/usr/bin/env python3
"""Verify shipped files against MANIFEST.json. Local edits will deliberately differ."""
from pathlib import Path
import hashlib
import json
import sys

def main() -> int:
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    if manifest.get('schema') != 'p4-manifest-v1':
        raise ValueError('Unsupported package manifest schema')
    failures = []
    for record in manifest['files']:
        path = (root / record['path']).resolve()
        if not path.is_relative_to(root):
            raise ValueError('Manifest path escapes the package directory')
        if not path.is_file():
            failures.append(record['path'] + ': missing')
            continue
        payload = path.read_bytes()
        if len(payload) != record['bytes'] or hashlib.sha256(payload).hexdigest() != record['sha256']:
            failures.append(record['path'] + ': changed')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        print('Differences may be expected after student edits. Preserve an original archive for comparison.', file=sys.stderr)
        return 1
    print(f"PASS: {len(manifest['files'])} shipped files match. Hashes check integrity, not publisher authenticity.")
    return 0
if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Manifest verification failed: {exc}', file=sys.stderr)
        raise SystemExit(2)
