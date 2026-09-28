"""Your Gate A implementation. This is an intentionally unfinished scaffold.

Choose your own architecture; meet CAPSTONE_SPEC.md. Do not import the reference.
Start with an explicit state dictionary and small pure functions.
"""

def initial_state():
    """Return a NEW starting state each time, not a shared mutable dictionary."""
    raise NotImplementedError('Design the state and write its invariants.')

def update(state,command):
    """Return the next state without printing or reading input."""
    raise NotImplementedError('Implement one complete transition.')

def render(state):
    """Return text without changing state."""
    raise NotImplementedError('Implement a read-only display.')

def main():
    """Connect input -> update -> output; handle restart and quit."""
    raise NotImplementedError('Build a small working loop, then add features.')

if __name__=='__main__':
    main()
