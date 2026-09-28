TRANSITIONS = {
    ("idle", "move"): "moving",
    ("moving", "stop"): "idle",
    ("idle", "hit"): "stunned",
    ("moving", "hit"): "stunned",
    ("stunned", "recover"): "idle",
}

def transition(state, event):
    """Unknown state is an error; an unlisted event leaves a valid state alone."""
    if state not in {"idle", "moving", "stunned"}:
        raise ValueError("unknown controller state")
    return TRANSITIONS.get((state, event), state)
