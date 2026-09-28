import json

def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result

def _validate(state):
    if type(state) is not dict or set(state) != {"version", "x", "health"}:
        raise ValueError("expected version, x and health fields only")
    if any(type(state[k]) is not int for k in state):
        raise ValueError("fields must be integers, not booleans")
    if state["version"] != 1:
        raise ValueError("unsupported version")
    if not -1000 <= state["x"] <= 1000 or not 0 <= state["health"] <= 100:
        raise ValueError("state values outside the documented limits")
    return dict(state)

def encode_save(state):
    """Validate then serialize one small flat save; never writes a file."""
    return json.dumps(_validate(state), sort_keys=True, allow_nan=False)

def decode_save(text):
    """At most 10,000 text characters; validate before returning a new state."""
    if type(text) is not str or len(text) > 10000:
        raise ValueError("save must be a small text string")
    candidate = json.loads(text, object_pairs_hook=_pairs)
    return _validate(candidate)
