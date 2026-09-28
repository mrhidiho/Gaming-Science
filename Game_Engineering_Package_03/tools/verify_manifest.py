"""Check hashes in the supplied manifest against an unmodified extracted bundle.

A checksum detects byte changes relative to this manifest; it is not a digital
signature or a guarantee about the author's identity. Intentional student edits
will appropriately change the corresponding hashes. Unlisted output files are
not checked, so generated work can live beside the course.
"""
from pathlib import Path
import hashlib
import json
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text())
        failures = []
        for entry in manifest['files']:
            relative = Path(entry['path'])
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('unsafe path in manifest')
            path = root / relative
            if not path.is_file():
                failures.append(str(relative) + ': missing')
                continue
            raw = path.read_bytes()
            if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
                failures.append(str(relative) + ': changed')
        if failures:
            print('\n'.join(failures))
            print('Intentional learner edits change hashes; retain the original ZIP for comparison.')
            return 1
        print(f"Verified {len(manifest['files'])} listed files; the manifest excludes itself.")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('Manifest verification stopped:', error)
        return 2


if __name__ == '__main__':
    sys.exit(main())
