def bounded_move(position, delta, size):
    """Trusted integer inputs; position within [0,size). Reject out-of-bounds move."""
    if size <= 0 or not 0 <= position < size:
        raise ValueError("invalid starting board/position")
    candidate = position + delta
    if 0 <= candidate < size:
        return candidate
    return position
