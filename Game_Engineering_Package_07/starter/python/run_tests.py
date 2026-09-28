"""Run exercise/reference contract cases. No third-party packages required.

Examples: python run_tests.py --target references
          python run_tests.py --target exercises --lesson 26.1
An unimplemented starter fails deliberately; it is never counted as a pass.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

def load(lesson: str, target: str = 'references'):
    path = ROOT / target / ('lesson_' + lesson.replace('.', '_') + '.py')
    spec = importlib.util.spec_from_file_location('lesson_' + lesson.replace('.', '_'), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Cannot load {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve

def equivalent(actual: object, expected: object) -> bool:
    if isinstance(expected, bool) or expected is None or isinstance(expected, str):
        return type(actual) is type(expected) and actual == expected
    if isinstance(expected, (int, float)):
        return not isinstance(actual, bool) and isinstance(actual, (int, float)) and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(equivalent(a,b) for a,b in zip(actual, expected))
    if isinstance(expected, dict):
        return isinstance(actual, dict) and actual.keys() == expected.keys() and all(equivalent(actual[k], v) for k,v in expected.items())
    return actual == expected

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=('references', 'exercises'), default='references')
    parser.add_argument('--lesson', help='For example: 26.1')
    args = parser.parse_args()
    bank = json.loads((ROOT/'cases.json').read_text())
    if args.lesson and args.lesson not in bank:
        parser.error('Unknown lesson ID')
    passed = failed = 0
    for lesson, item in bank.items():
        if args.lesson and lesson != args.lesson:
            continue
        solve = load(lesson, args.target)
        for index, case in enumerate(item['cases'], 1):
            try:
                value = solve(case['input'])
                if 'error' in case:
                    raise AssertionError(f"Expected {case['error']}, returned {value!r}")
                if not equivalent(value, case['output']):
                    raise AssertionError(f"Expected {case['output']!r}; got {value!r}")
            except Exception as exc:
                if 'error' in case and type(exc).__name__ == case['error']:
                    passed += 1
                    continue
                failed += 1
                print(f'FAIL {lesson} case {index}: {type(exc).__name__}: {exc}')
            else:
                passed += 1
    print(f'{args.target}: {passed} passed, {failed} failed')
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
