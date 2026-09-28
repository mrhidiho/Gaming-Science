def trace_moves(start, deltas):
    """Return the initial integer position and each following position."""
    position = start
    trace = [position]
    for delta in deltas:
        position = position + delta
        trace.append(position)
    return trace
