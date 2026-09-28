"""Check the designated coding exercise, not the lesson's proofs or entire project."""
from pathlib import Path
import argparse
import importlib.util
import math
import sys
import unittest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
from lab_cases import CASES

def load_module(path):
    spec=importlib.util.spec_from_file_location('chosen_lab_'+path.stem,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def compare(test, actual, expected):
    if isinstance(expected, bool):
        test.assertIs(actual,expected)
    elif isinstance(expected,float):
        test.assertIsInstance(actual,(int,float))
        test.assertTrue(math.isfinite(actual) and math.isclose(actual,expected,rel_tol=1e-8,abs_tol=1e-9),f'{actual!r} != {expected!r} within tolerance')
    elif isinstance(expected,dict):
        test.assertIsInstance(actual,dict)
        for key,value in expected.items():
            test.assertIn(key,actual)
            compare(test,actual[key],value)
    elif isinstance(expected,(list,tuple)):
        test.assertIsInstance(actual,(list,tuple))
        test.assertEqual(len(actual),len(expected))
        for a,e in zip(actual,expected): compare(test,a,e)
    else:
        test.assertEqual(actual,expected)

def make_suite(lessons,reference=False,overrides=None):
    modules={}
    for lesson in lessons:
        path=ROOT/'labs'/('reference' if reference else 'student')/('lab_'+lesson.replace('.','_')+'.py')
        modules[lesson]=load_module(path) if not overrides or lesson not in overrides else overrides[lesson]
    cls=type('LabContractChecks',(unittest.TestCase,),{})
    for i,case in enumerate(CASES):
        if case.lesson not in modules:continue
        def test(self,case=case):
            function=getattr(modules[case.lesson],case.function)
            if case.error:
                with self.assertRaises(case.error):function(*case.args)
            else:compare(self,function(*case.args),case.expected)
        setattr(cls,f'test_{case.lesson.replace(".","_")}_{i:03}_{case.name}',test)
    return unittest.defaultTestLoader.loadTestsFromTestCase(cls)

def main():
    ids=sorted(set(c.lesson for c in CASES))
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson',nargs='?',choices=ids)
    parser.add_argument('--all',action='store_true')
    parser.add_argument('--reference',action='store_true',help='check supplied reference exports instead of your work')
    args=parser.parse_args()
    if bool(args.lesson)==args.all:parser.error('choose one lesson or --all')
    if not args.reference:print('Student stubs are intentionally unfinished. Code checks do not grade written reasoning.',flush=True)
    result=unittest.TextTestRunner(verbosity=2).run(make_suite(ids if args.all else [args.lesson],args.reference))
    return 0 if result.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
