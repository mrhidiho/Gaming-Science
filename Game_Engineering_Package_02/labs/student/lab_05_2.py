# Student exercise. Expected to fail checks until implemented.
OBSTACLES = {(1, 1), (3, 2), (4, 4), (7, 6), (8, 8)}
DELTAS = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

def step_world(world, command):
    """Valid flat {x,y,won} state on a fixed 10x10 map; no mutation.

Obstacles and edges reject the whole move. Once won, all commands no-op.
This teaching model omits the capstone's energy and restart rules."""
    raise NotImplementedError('Implement Lesson 05.2; see the lab workbook.')
