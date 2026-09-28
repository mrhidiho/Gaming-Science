"""Pure deterministic rules. No terminal, clock, randomness or filesystem I/O."""
from dataclasses import dataclass, replace

WIDTH=HEIGHT=10
GOAL=(9,9)
OBSTACLES=frozenset({(1,1),(3,2),(4,4),(7,6),(8,8)})
START_ENERGY=25
RULES_ID='training-yard-v1'
DELTAS={'w':(0,-1),'a':(-1,0),'s':(0,1),'d':(1,0),'wait':(0,0)}
STATUSES=frozenset({'playing','won','lost','quit'})

@dataclass(frozen=True)
class State:
    x: int=0
    y: int=0
    energy: int=START_ENERGY
    turns: int=0
    status: str='playing'

def validate(state):
    if not isinstance(state,State):
        raise ValueError('expected State')
    if any(type(v) is not int for v in (state.x,state.y,state.energy,state.turns)):
        raise ValueError('coordinates, energy and turns must be integers')
    if not (0 <= state.x < WIDTH and 0 <= state.y < HEIGHT):
        raise ValueError('position outside the map')
    if (state.x,state.y) in OBSTACLES:
        raise ValueError('position is inside an obstacle')
    if not (0 <= state.turns <= START_ENERGY
            and state.energy == START_ENERGY-state.turns):
        raise ValueError('energy/turn invariant failed')
    if type(state.status) is not str or state.status not in STATUSES:
        raise ValueError('unknown status')
    at_goal=(state.x,state.y)==GOAL
    if state.status=='won' and not at_goal:
        raise ValueError('won requires the goal position')
    if state.status!='won' and at_goal:
        raise ValueError('goal position requires won status')
    if state.status in {'playing','quit'} and state.energy==0:
        raise ValueError('playing or quit requires positive energy')
    if state.status=='lost' and state.energy!=0:
        raise ValueError('lost requires zero energy')
    return state

def normalise(command):
    if type(command) is not str or len(command)>256:
        raise ValueError('command must be text of at most 256 characters')
    return command.strip().lower()

def step(state,command):
    """Return (state, message). Rejected moves are complete no-ops.

    Restart is allowed in all states. Other actions after terminal states no-op.
    Legal movement/wait costs one energy. Reaching goal wins even at zero energy.
    """
    validate(state)
    command=normalise(command)
    if command=='r':
        return State(),'Restarted.'
    if state.status!='playing':
        return state,'Round finished. Use r to restart or q to leave the terminal.'
    if command=='q':
        return replace(state,status='quit'),'Quit.'
    if command not in DELTAS:
        return state,'Unknown command. Use w/a/s/d, wait, r or q.'
    dx,dy=DELTAS[command]
    x,y=state.x+dx,state.y+dy
    if not (0<=x<WIDTH and 0<=y<HEIGHT):
        return state,'Edge: no movement or energy cost.'
    if (x,y) in OBSTACLES:
        return state,'Obstacle: no movement or energy cost.'
    energy=state.energy-1
    status='won' if (x,y)==GOAL else ('lost' if energy==0 else 'playing')
    candidate=State(x,y,energy,state.turns+1,status)
    validate(candidate)
    return candidate, {'won':'You reached the exit!',
                       'lost':'Out of energy. Use r to restart.',
                       'playing':'Waited.' if command=='wait' else 'Moved.'}[status]

def render(state):
    """Return an ASCII snapshot. Calling repeatedly never advances the world."""
    validate(state)
    rows=[]
    for y in range(HEIGHT):
        cells=[]
        for x in range(WIDTH):
            point=(x,y)
            token='P' if point==(state.x,state.y) else (
                '#' if point in OBSTACLES else ('E' if point==GOAL else '.'))
            cells.append(token)
        rows.append(''.join(cells))
    return '\n'.join(rows)+f'\nEnergy={state.energy} Turns={state.turns} Status={state.status}'

def replay(commands,initial=None):
    state=State() if initial is None else validate(initial)
    for command in commands:
        state,_=step(state,command)
    return state
