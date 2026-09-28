"""Run all supplied reference checks. This does not mark student work complete."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
import check_lab
import test_reference

def main():
    ids=[f'{m:02}.{i}' for m in range(6,11) for i in range(1,5)]
    suite=unittest.TestSuite([check_lab.make_suite(ids,True),unittest.defaultTestLoader.loadTestsFromModule(test_reference)])
    print('Reference code validation only: written proofs, real-platform coverage and student mastery are not certified.',flush=True)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
