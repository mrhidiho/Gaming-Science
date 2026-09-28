OBSTACLES = {(1, 1), (3, 2), (4, 4), (7, 6), (8, 8)}
DELTAS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}

def step_world(world, command):
    """Valid flat {x,y,won} state on a fixed 10x10 map; no mutation.

    Obstacles and edges reject the whole move. Once won, all commands no-op.
    This teaching model omits the capstone's energy and restart rules.
    """
    result = dict(world)
    if world["won"]:
        return result
    delta = DELTAS.get(command.strip().lower())
    if delta is None:
        return result
    x, y = world["x"] + delta[0], world["y"] + delta[1]
    if not (0 <= x < 10 and 0 <= y < 10) or (x, y) in OBSTACLES:
        return result
    result["x"], result["y"] = x, y
    result["won"] = (x, y) == (9, 9)
    return result
