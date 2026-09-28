# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import posterior_bug
bug_count = 100
nonbug_count = 9900
true_alerts = int(bug_count * 0.9)
false_alerts = int(nonbug_count * 0.05)
print("true and false alerts:", true_alerts, false_alerts)
print(f"P(bug|alert): {posterior_bug(0.01, 0.9, 0.05):.6f}")
print("independent two heads:", 0.5 * 0.5)
print("copied second coin, two heads:", 0.5)
