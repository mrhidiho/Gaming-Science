import hashlib
import json
from lab_05_2 import step_world

def replay(commands):
    """Replay on the Lesson 05.2 map from the fixed initial state."""
    state = {"x": 0, "y": 0, "won": False}
    for command in commands:
        state = step_world(state, command)
    return state

def state_digest(state):
    """Canonical serialization digest for comparison, not a correctness proof."""
    payload = json.dumps(state, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
