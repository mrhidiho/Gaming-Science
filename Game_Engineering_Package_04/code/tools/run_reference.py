#!/usr/bin/env python3
"""Configure, build and test the Package 04 reference code. No downloads/installers."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build', type=Path, default=Path('build/debug'))
    p.add_argument('--config', choices=['Debug', 'Release'], default='Debug')
    p.add_argument('--sanitize', action='store_true')
    args = p.parse_args()
    for executable in ('cmake', 'ctest'):
        if not shutil.which(executable):
            p.error(f'{executable} is not in PATH; install/configure the documented toolchain first.')
    source = Path(__file__).resolve().parents[1]
    build = args.build.resolve()
    commands = [
        ['cmake', '-S', str(source), '-B', str(build), '-DCMAKE_BUILD_TYPE=' + args.config,
         '-DP4_SANITIZE=' + ('ON' if args.sanitize else 'OFF')],
        ['cmake', '--build', str(build), '--config', args.config, '--parallel', '2'],
        ['ctest', '--test-dir', str(build), '-C', args.config, '-L', 'reference', '--output-on-failure']]
    for command in commands:
        print('+', ' '.join(command), flush=True)
        subprocess.run(command, check=True)
    return 0
if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f'Reference workflow failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
