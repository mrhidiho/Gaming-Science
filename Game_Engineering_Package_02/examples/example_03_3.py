# Worked demonstration for Lesson 03.3.
import json

original = {"version": 1, "x": 2, "health": 90}
text = json.dumps(original, sort_keys=True)
candidate = json.loads(text)
print("encoded:", text)
print("same values:", candidate == original)
print("independent dictionary:", candidate is not original)

live = dict(original)
try:
    live = json.loads('{"version":')
except json.JSONDecodeError:
    print("Rejected truncated JSON; live health:", live["health"])
