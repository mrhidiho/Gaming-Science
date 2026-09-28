"""Terminal adapter. Only this layer prompts, prints and chooses save locations."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
from .model import State,normalise,render,replay,step
from .storage import MAX_COMMANDS,load,read_replay,save,write_replay

HELP='w/a/s/d move | wait | r restart | q quit | help | save | load | export'

def main(argv=None):
    parser=argparse.ArgumentParser(description='Training Yard reference game')
    parser.add_argument('--demo',action='store_true',help='run a known winning replay')
    parser.add_argument('--replay',type=Path,help='validate and replay a JSON recording')
    args=parser.parse_args(argv)
    if args.demo:
        final=replay(['d']*9+['s']*9)
        print(render(final))
        return 0
    if args.replay is not None:
        try:
            initial,commands=read_replay(args.replay)
            print(json.dumps(asdict(replay(commands,initial)),sort_keys=True))
            return 0
        except (OSError,ValueError) as exc:
            print('Replay failed:',exc)
            return 2
    state=State()
    session_initial=state
    history=[]
    workspace=Path.cwd()/'workspace'
    print('TRAINING YARD - reach E before energy runs out. P=player #=obstacle')
    print(HELP)
    print(render(state))
    while True:
        try:
            raw=input('command> ')
        except (EOFError,KeyboardInterrupt):
            print('\nExited. Save explicitly during play to keep progress.')
            return 0
        try:
            command=normalise(raw)
            if command=='help':
                print(HELP)
                continue
            if command=='save':
                workspace.mkdir(exist_ok=True)
                save(workspace/'save.json',state)
                print('Saved:',workspace/'save.json')
                continue
            if command=='load':
                candidate=load(workspace/'save.json')
                state=candidate
                session_initial=state
                history=[]
                print('Loaded; a new replay segment starts here.')
                print(render(state))
                continue
            if command=='export':
                workspace.mkdir(exist_ok=True)
                write_replay(workspace/'replay.json',session_initial,history)
                print('Exported:',workspace/'replay.json')
                continue
            # Segment before the next action; current state is the new initial state.
            if len(history)==MAX_COMMANDS:
                session_initial=state
                history=[]
                print('Replay buffer full: starting a new segment from current state.')
            history.append(command)
            state,message=step(state,command)
            print(message)
            print(render(state))
            if command=='q':
                return 0
        except (OSError,ValueError) as exc:
            print('Action failed; current game state preserved:',exc)
