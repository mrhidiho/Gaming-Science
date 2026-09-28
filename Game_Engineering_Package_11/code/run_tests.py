#!/usr/bin/env python3
"""Run reference checks or the intentionally incomplete student contracts."""
import argparse,json,os,sys,unittest
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--student',action='store_true')
    parser.add_argument('--report',type=Path,help='Optional JSON result destination')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    sys.path.insert(0,str(root))
    if args.student:
        os.environ['V10_IMPLEMENTATION']='student'
        suite=unittest.defaultTestLoader.loadTestsFromName('tests.test_exercises')
    else:
        os.environ['V10_IMPLEMENTATION']='reference'
        suite=unittest.defaultTestLoader.discover(str(root/'tests'),top_level_dir=str(root))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    data=dict(implementation='student' if args.student else 'reference',
              tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),
              skipped=len(result.skipped),passed=result.wasSuccessful(),
              note='Counts are test methods; exhaustive subcases are additional, not separate methods.')
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(data,indent=2)+'\n')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
