#!/usr/bin/env python3
"""Controlled GCC/Clang-style compile/link experiments. Never executes broken code."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cxx', default=os.environ.get('CXX', 'c++'),
                        help='GCC/Clang-style compiler executable, not a flags string')
    args = parser.parse_args()
    compiler = shutil.which(args.cxx)
    if not compiler:
        parser.error(f'Compiler not found: {args.cxx}')
    fixtures = Path(__file__).resolve().parents[1] / 'fixtures'
    with tempfile.TemporaryDirectory(prefix='p4_build_lesson_') as folder:
        work = Path(folder)
        for name, syntax_only, expected_success in [
            ('good', False, True), ('compile_error', True, False), ('link_error', False, False)]:
            source = work / (name + '.cpp')
            source.write_text((fixtures / (name + '.txt')).read_text(encoding='utf-8'), encoding='utf-8')
            command = [compiler, '-std=c++20', '-Wall', '-Wextra', '-Wpedantic']
            command += ['-fsyntax-only', str(source)] if syntax_only else [str(source), '-o', str(work / name)]
            print('\nEXPERIMENT:', name, '\nCOMMAND:', ' '.join(command), flush=True)
            completed = subprocess.run(command, text=True, capture_output=True, timeout=30)
            print(completed.stdout + completed.stderr)
            if (completed.returncode == 0) != expected_success:
                print('UNEXPECTED RESULT; check the compiler and experiment.', file=sys.stderr)
                return 1
            print('Expected success.' if expected_success else 'Expected rejection; now explain the stage.')
    return 0
if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f'Experiment could not complete: {exc}', file=sys.stderr)
        raise SystemExit(2)
