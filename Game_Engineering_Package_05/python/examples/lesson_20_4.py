from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
old="ERROR: invalid"
new="REQ_VERSION: expected version 1. Check the request template and retry."
print("Before:",old)
print("After:",new)
print("Review: text-only status, actionable recovery, no secret or full payload in the message.")
