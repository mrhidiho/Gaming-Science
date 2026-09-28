import dataclasses
import io
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REFERENCE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REFERENCE))
from yard import model,storage
from yard.model import State,step,replay,render,validate

class ModelTests(unittest.TestCase):
    def test_initial_valid(self):
        self.assertEqual(validate(State()),State())
    def test_one_move_one_turn(self):
        self.assertEqual(step(State(),'d')[0],State(1,0,24,1,'playing'))
    def test_input_normalisation(self):
        self.assertEqual(step(State(),' D ')[0],step(State(),'d')[0])
    def test_unknown_noop(self):
        self.assertEqual(step(State(),'launch')[0],State())
    def test_left_edge_noop(self):
        self.assertEqual(step(State(),'a')[0],State())
    def test_top_edge_noop(self):
        self.assertEqual(step(State(),'w')[0],State())
    def test_right_edge_noop(self):
        state=State(9,0,16,9,'playing')
        self.assertEqual(step(state,'d')[0],state)
    def test_bottom_edge_noop(self):
        state=State(0,9,16,9,'playing')
        self.assertEqual(step(state,'s')[0],state)
    def test_obstacle_no_partial_cost(self):
        state=step(State(),'d')[0]
        self.assertEqual(step(state,'s')[0],state)
    def test_wait_cost(self):
        self.assertEqual(step(State(),'wait')[0],State(0,0,24,1,'playing'))
    def test_win(self):
        self.assertEqual(replay(['d']*9+['s']*9),State(9,9,7,18,'won'))
    def test_loss(self):
        self.assertEqual(replay(['wait']*25),State(0,0,0,25,'lost'))
    def test_win_on_last_energy(self):
        commands=['wait']*7+['d']*9+['s']*9
        self.assertEqual(replay(commands),State(9,9,0,25,'won'))
    def test_after_win_noop(self):
        state=replay(['d']*9+['s']*9)
        self.assertEqual(step(state,'a')[0],state)
    def test_after_loss_noop(self):
        state=replay(['wait']*25)
        self.assertEqual(step(state,'d')[0],state)
    def test_restart_from_all_statuses(self):
        states=[State(),replay(['wait']*25),replay(['d']*9+['s']*9),step(State(),'q')[0]]
        for state in states:
            self.assertEqual(step(state,'r')[0],State())
    def test_quit_costs_nothing(self):
        self.assertEqual(step(State(),'q')[0],State(0,0,25,0,'quit'))
    def test_render_twice_is_readonly(self):
        state=State()
        self.assertEqual(render(state),render(state))
        self.assertEqual(state,State())
    def test_ascii_board(self):
        board=render(State()).splitlines()[:10]
        self.assertEqual(len(board),10)
        self.assertTrue(all(len(row)==10 for row in board))
        self.assertEqual(''.join(board).count('P'),1)
        self.assertEqual(''.join(board).count('#'),5)
        self.assertEqual(''.join(board).count('E'),1)
    def test_state_is_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            State().x=4
    def test_bad_state_range(self):
        with self.assertRaises(ValueError): validate(State(x=-1))
    def test_bad_energy_invariant(self):
        with self.assertRaises(ValueError): validate(State(energy=7))
    def test_bad_bool(self):
        with self.assertRaises(ValueError): validate(State(x=True))
    def test_bad_status(self):
        with self.assertRaises(ValueError): validate(State(status='winner'))
    def test_bad_won_position(self):
        with self.assertRaises(ValueError): validate(State(status='won'))
    def test_bad_obstacle(self):
        with self.assertRaises(ValueError): validate(State(x=1,y=1))
    def test_bad_command_type(self):
        with self.assertRaises(ValueError): step(State(),42)
    def test_bad_command_length(self):
        with self.assertRaises(ValueError): step(State(),'a'*257)
    def test_deterministic_replay(self):
        commands=['d']*9+['s']*9+['a','?']
        self.assertEqual(replay(commands),replay(commands))
    def test_generated_state_invariants(self):
        rng=random.Random(20260928)
        state=State()
        for _ in range(3000):
            state,_=step(state,rng.choice(['w','a','s','d','wait','r','q','?']))
            self.assertEqual(validate(state),state)
            self.assertTrue(0<=state.x<10 and 0<=state.y<10)
            self.assertNotIn((state.x,state.y),model.OBSTACLES)

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root=Path(self.directory.name)
        self.path=self.root/'save.json'
    def test_roundtrip(self):
        state=replay(['d','d','s'])
        storage.save(self.path,state)
        self.assertEqual(storage.load(self.path),state)
    def test_existing_save_replaced(self):
        storage.save(self.path,State())
        storage.save(self.path,step(State(),'d')[0])
        self.assertEqual(storage.load(self.path).x,1)
    def test_failed_replace_preserves_previous_save(self):
        storage.save(self.path,State())
        before=self.path.read_bytes()
        with patch('yard.storage.os.replace',side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                storage.save(self.path,step(State(),'d')[0])
        self.assertEqual(self.path.read_bytes(),before)
        self.assertEqual(list(self.root.iterdir()),[self.path])
    def test_bad_state_cannot_replace_save(self):
        storage.save(self.path,State())
        before=self.path.read_bytes()
        with self.assertRaises(ValueError): storage.save(self.path,State(x=-1))
        self.assertEqual(self.path.read_bytes(),before)
    def test_missing_file(self):
        with self.assertRaises(OSError): storage.load(self.path)
    def test_oversized_file(self):
        self.path.write_bytes(b' '*(storage.MAX_BYTES+1))
        with self.assertRaises(ValueError): storage.load(self.path)
    def test_truncated_file(self):
        self.path.write_text('{"version":',encoding='utf-8')
        with self.assertRaises(ValueError): storage.load(self.path)
    def test_utf8_required(self):
        self.path.write_bytes(b'\xff')
        with self.assertRaises(ValueError): storage.load(self.path)
    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError): storage.parse('{"x":1,"x":2}')
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): storage.parse('{"x":NaN}')
    def test_boolean_version_rejected(self):
        payload=storage.pack_state(State());payload['version']=True
        with self.assertRaises(ValueError): storage.unpack_state(payload)
    def test_unknown_version_rejected(self):
        payload=storage.pack_state(State());payload['version']=999
        with self.assertRaises(ValueError): storage.unpack_state(payload)
    def test_extra_field_rejected(self):
        payload=storage.pack_state(State());payload['cheat']=True
        with self.assertRaises(ValueError): storage.unpack_state(payload)
    def test_wrong_rules_rejected(self):
        payload=storage.pack_state(State());payload['rules']='different-map'
        with self.assertRaises(ValueError): storage.unpack_state(payload)
    def test_nonstring_status_rejected(self):
        payload=storage.pack_state(State());payload['state']['status']=[]
        with self.assertRaises(ValueError): storage.unpack_state(payload)
    def test_replay_roundtrip(self):
        commands=['d']*9+['s']*9
        storage.write_replay(self.path,State(),commands)
        initial,loaded=storage.read_replay(self.path)
        self.assertEqual(replay(loaded,initial),State(9,9,7,18,'won'))
    def test_replay_keeps_nondefault_initial(self):
        initial=step(State(),'d')[0]
        storage.write_replay(self.path,initial,['d'])
        loaded,commands=storage.read_replay(self.path)
        self.assertEqual(replay(commands,loaded),State(2,0,23,2,'playing'))
    def test_replay_command_limit(self):
        with self.assertRaises(ValueError):
            storage.write_replay(self.path,State(),['d']*1001)
    def test_replay_invalid_command_type(self):
        with self.assertRaises(ValueError): storage.write_replay(self.path,State(),[3])
    def test_replay_read_limit(self):
        data={'version':1,'rules':model.RULES_ID,
              'initial':storage.pack_state(State()),'commands':['d']*1001}
        self.path.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaises(ValueError): storage.read_replay(self.path)
    def test_failed_load_keeps_live_state(self):
        live=step(State(),'d')[0]
        before=live
        self.path.write_text('bad json',encoding='utf-8')
        try:
            live=storage.load(self.path)
        except ValueError:
            pass
        self.assertEqual(live,before)

class CommandLineTests(unittest.TestCase):
    def run_cli(self,*args,input_text=None,cwd=None):
        return subprocess.run([sys.executable,str(REFERENCE/'play.py'),*args],
            cwd=cwd,input=input_text,capture_output=True,text=True,timeout=10)
    def test_demo(self):
        result=self.run_cli('--demo')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('Energy=7 Turns=18 Status=won',result.stdout)
    def test_help(self):
        result=self.run_cli('--help')
        self.assertEqual(result.returncode,0)
        self.assertIn('--replay',result.stdout)
    def test_interactive_quit(self):
        result=self.run_cli(input_text='d\nq\n')
        self.assertEqual(result.returncode,0)
        self.assertIn('Status=quit',result.stdout)
    def test_eof_exits(self):
        result=self.run_cli(input_text='')
        self.assertEqual(result.returncode,0)
        self.assertIn('Exited.',result.stdout)
    def test_save_load_export(self):
        with tempfile.TemporaryDirectory() as directory:
            result=self.run_cli(input_text='d\nsave\nr\nload\nexport\nq\n',cwd=directory)
            self.assertEqual(result.returncode,0,result.stderr)
            workspace=Path(directory)/'workspace'
            self.assertEqual(storage.load(workspace/'save.json').x,1)
            initial,commands=storage.read_replay(workspace/'replay.json')
            self.assertEqual(initial.x,1)
            self.assertEqual(commands,[])
    def test_replay_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'replay.json'
            storage.write_replay(path,State(),['d']*9+['s']*9)
            result=self.run_cli('--replay',str(path))
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'],'won')
    def test_bad_replay_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            result=self.run_cli('--replay',str(Path(directory)/'missing.json'))
            self.assertEqual(result.returncode,2)
            self.assertIn('Replay failed',result.stdout)
    def test_import_does_not_prompt(self):
        result=subprocess.run([sys.executable,'-c','import yard.model; import yard.cli'],
            cwd=REFERENCE,capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout,'')

if __name__=='__main__':
    unittest.main()
