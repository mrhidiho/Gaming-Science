# Student exercise. Expected to fail checks until implemented.
DELTAS = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

def normalise_command(text):
    """Text command -> stripped lowercase text."""
    raise NotImplementedError('Implement Lesson 05.1; see the lab workbook.')

def step_position(position, command, size=10):
    """Valid integer tuple position; known legal move or unchanged position."""
    raise NotImplementedError('Implement Lesson 05.1; see the lab workbook.')

def render_grid(position, size=10):
    """Return exactly size rows; P is the player; E is the bottom-right exit; other cells are dots."""
    raise NotImplementedError('Implement Lesson 05.1; see the lab workbook.')
