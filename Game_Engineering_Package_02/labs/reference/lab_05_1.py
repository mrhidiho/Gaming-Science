DELTAS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}

def normalise_command(text):
    """Text command -> stripped lowercase text."""
    return text.strip().lower()

def step_position(position, command, size=10):
    """Valid integer tuple position; known legal move or unchanged position."""
    x, y = position
    if size < 1 or not (0 <= x < size and 0 <= y < size):
        raise ValueError("invalid starting position")
    delta = DELTAS.get(normalise_command(command))
    if delta is None:
        return position
    nx, ny = x + delta[0], y + delta[1]
    if 0 <= nx < size and 0 <= ny < size:
        return nx, ny
    return position

def render_grid(position, size=10):
    """Return exactly size rows; P is the player; E is the bottom-right exit; other cells are dots."""
    x, y = position
    if size < 1 or not (0 <= x < size and 0 <= y < size):
        raise ValueError("invalid starting position")
    rows = []
    for row in range(size):
        cells = []
        for column in range(size):
            cells.append("P" if (column, row) == position else (
                "E" if (column, row) == (size - 1, size - 1) else "."))
        rows.append("".join(cells))
    return "\n".join(rows)
