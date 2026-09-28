"""Validate ledger file existence and hashes. This is not scientific peer review."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ALLOWED={'analytical','functional_model','cycle_model','synthesis','host_measurement','physical_measurement'}

def audit(ledger_path: Path) -> list[str]:
    ledger_path=ledger_path.resolve(); root=ledger_path.parent; issues=[]; ids=set()
    records=json.loads(ledger_path.read_text())
    if not isinstance(records,list) or not records: return ['ledger must be a nonempty list']
    for record in records:
        identity=record.get('id','')
        if not identity or identity in ids: issues.append('missing or duplicate id')
        ids.add(identity)
        for key in ['claim','requirement','limitations']:
            if not record.get(key): issues.append(f'{identity}: missing {key}')
        if record.get('tier') not in ALLOWED: issues.append(f'{identity}: invalid tier')
        rel=record.get('artifact','')
        path=(root/rel).resolve()
        if not rel or not path.is_relative_to(root) or not path.is_file():
            issues.append(f'{identity}: invalid or absent artifact'); continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=record.get('sha256'): issues.append(f'{identity}: checksum mismatch')
    return issues

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger',type=Path); args=parser.parse_args()
    issues=audit(args.ledger)
    print('\n'.join(issues) if issues else 'Ledger files and hashes verified; substantive claims require review.')
    return 1 if issues else 0
if __name__=='__main__': raise SystemExit(main())
