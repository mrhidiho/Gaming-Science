#!/usr/bin/env python3
"""Independent Python transition fixture for E11.8; not the learner's earlier game."""
import csv
import io
from pathlib import Path
import sys

def replay() -> str:
    x, y = 0, 0
    output = io.StringIO(newline='')
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['command', 'dx', 'dy', 'x', 'y', 'accepted'])
    for index, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, 1), (0, 0), (1, 0), (1, 0)], 1):
        nx, ny = x + dx, y + dy
        accepted = 0 <= nx < 3 and 0 <= ny < 3
        if accepted:
            x, y = nx, ny
        writer.writerow([index, dx, dy, x, y, int(accepted)])
    return output.getvalue()
if __name__ == '__main__':
    expected = Path(__file__).resolve().parents[2] / 'data' / 'grid_trace.csv'
    actual = replay()
    if actual != expected.read_text(encoding='utf-8'):
        print('FAIL: generated trace differs from checked-in golden data.', file=sys.stderr)
        raise SystemExit(1)
    print(actual, end='')
    print('PASS Python golden replay', file=sys.stderr)
