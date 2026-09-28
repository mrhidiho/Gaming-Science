"""A tiny complete game for Modules 03-05. No network or file writes.

Run: python3 grid_game.py
Replay: python3 grid_game.py --replay SSSSDDDDDD
Commands W/A/S/D attempt one move. A blocked move consumes a turn.
Invalid commands do not change state. After victory, state stays unchanged.
"""
import argparse
from dataclasses import dataclass

WIDTH, HEIGHT = 7, 5
GOAL = (6, 4)
WALLS = frozenset({(2, 0), (2, 1), (2, 2), (4, 2), (5, 2), (4, 3)})
DIRECTIONS = {"W": (0, -1), "A": (-1, 0), "S": (0, 1), "D": (1, 0)}


@dataclass(frozen=True)
class GameState:
    x: int = 0
    y: int = 0
    turn: int = 0

    def __post_init__(self):
        if any(type(v) is not int for v in (self.x, self.y, self.turn)):
            raise TypeError("coordinates and turn must be integers")
        if not (0 <= self.x < WIDTH and 0 <= self.y < HEIGHT):
            raise ValueError("position is outside the world")
        if (self.x, self.y) in WALLS or self.turn < 0:
            raise ValueError("state must not start inside a wall or at a negative turn")

    @property
    def won(self) -> bool:
        return (self.x, self.y) == GOAL


def step(state: GameState, command: str) -> GameState:
    if not isinstance(command, str) or command.upper() not in DIRECTIONS:
        raise ValueError("use one command: W, A, S or D")
    if state.won:
        return state
    dx, dy = DIRECTIONS[command.upper()]
    nx, ny = state.x + dx, state.y + dy
    if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT) or (nx, ny) in WALLS:
        nx, ny = state.x, state.y
    return GameState(nx, ny, state.turn + 1)


def render(state: GameState) -> str:
    """Observe state only. Rendering does not advance a turn."""
    rows = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            cell = "#" if (x, y) in WALLS else "."
            if (x, y) == GOAL:
                cell = "G"
            if (x, y) == (state.x, state.y):
                cell = "P"
            row.append(cell)
        rows.append(" ".join(row))
    return "\n".join(rows) + f"\nTurn {state.turn}; position=({state.x}, {state.y})"


def replay(commands: str) -> GameState:
    state = GameState()
    for command in commands:
        state = step(state, command)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Reach G using W/A/S/D. # is a wall.")
    parser.add_argument("--replay", help="replay a command string, such as SSSSDDDDDD")
    args = parser.parse_args()
    if args.replay is not None:
        try:
            state = replay(args.replay)
        except ValueError as exc:
            parser.error(str(exc))
        print(render(state))
        print("You reached the goal!" if state.won else "Replay ended before the goal.")
        return 0
    state = GameState()
    print("Reach G. W/A/S/D moves; Q quits. Blocked moves use a turn.")
    while True:
        print(render(state))
        if state.won:
            print("You reached the goal!")
            return 0
        try:
            command = input("Move: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nGame closed.")
            return 0
        if command == "Q":
            return 0
        try:
            state = step(state, command)
        except ValueError as exc:
            print(exc)


if __name__ == "__main__":
    raise SystemExit(main())
