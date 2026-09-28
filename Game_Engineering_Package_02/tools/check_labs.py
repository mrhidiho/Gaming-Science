"""Run supplied contract checks, not a substitute for learner-written tests.

From the package root:
  python3 tools/check_labs.py --lesson 02.4
  python3 tools/check_labs.py --reference
"""
import argparse
import importlib
import io
import json
import math
from pathlib import Path
import sys
import unittest
from contextlib import redirect_stdout

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reference', action='store_true')
parser.add_argument('--lesson', help='A lesson ID, for example 02.4')
args = parser.parse_args()
folder = ROOT / 'labs' / ('reference' if args.reference else 'student')
sys.path.insert(0, str(folder))

class Contracts(unittest.TestCase):
    pass

COUNTS = {}
def add(lid, name, function):
    if args.lesson and lid != args.lesson:
        return
    def run(self):
        module = importlib.import_module('lab_' + lid.replace('.', '_'))
        function(self, module)
    setattr(Contracts, 'test_' + lid.replace('.', '_') + '_' + name, run)
    COUNTS[lid] = COUNTS.get(lid, 0) + 1

def equals(lid, name, function, inputs, expected):
    def run(t, m):
        actual = getattr(m, function)(*inputs)
        if isinstance(expected, float):
            t.assertAlmostEqual(actual, expected)
        else:
            t.assertEqual(actual, expected)
    add(lid, name, run)

def rejects(lid, name, function, inputs):
    def run(t, m):
        with t.assertRaises(ValueError):
            getattr(m, function)(*inputs)
    add(lid, name, run)

for name, start, moves, result in [
 ('original',2,[3,-1,0,-4,2],[2,5,4,4,0,2]),
 ('empty',7,[],[7]), ('negative',-2,[-3,1],[-2,-5,-4])]:
    equals('01.1',name,'trace_moves',(start,moves),result)
for name, a, b in [('different',3,8),('same',4,4),('text','left','right')]:
    equals('01.3',name,'swap_values',(a,b),(b,a))
for n,s,d,e in [('distance',8,.125,1.0),('zero',8,0,0.0),('negative_speed',-3,2,-6.0)]:
    equals('01.4',n,'displacement',(s,d),e)
for n,v in [('bad_dt',-1),('nan_dt',float('nan')),('infinite_dt',float('inf'))]:
    rejects('01.4',n,'displacement',(8,v))
for n,f,e in [('sixty',60,1000/60),('one_twenty',120,1000/120)]:
    equals('01.4',n,'frame_interval_ms',(f,),e)
for n,f in [('zero_fps',0),('negative_fps',-1),('infinite_fps',float('inf'))]:
    rejects('01.4',n,'frame_interval_ms',(f,))
for n,c,p,e in [('normal','3','4',12),('zero','0','9',0),('spaces',' 2 ','5',10)]:
    equals('02.1',n,'total_cost',(c,p),e)
for n,c,p in [('bad_text','many','4'),('fraction','2.5','4'),('negative','-1','4'),('negative_price','2','-4')]:
    rejects('02.1',n,'total_cost',(c,p))
for key in [False,True]:
    for level in [4,5,6]:
        for stamina in [9,10,11]:
            expected = True if key else (level != 4 and stamina != 9)
            equals('02.2',f'key{int(key)}_level{level}_stamina{stamina}',
                   'can_open',(key,level,stamina),expected)
equals('02.3','zero','simulate_resources',(0,),[0])
equals('02.3','ten','simulate_resources',(10,),[0,3,1,4,2,0,3,1,4,2,0])
rejects('02.3','negative','simulate_resources',(-1,))
rejects('02.3','bool','simulate_resources',(True,))
def resource_property(t,m):
    for turns in range(51):
        result=m.simulate_resources(turns)
        t.assertEqual(len(result), turns+1)
        t.assertTrue(all(0 <= x < 5 for x in result))
add('02.3','bounded_property_51_inputs',resource_property)
for n,inputs,e in [('normal',(2,6,.25),3.5),('stationary',(2,0,3),2.0),
                   ('negative_velocity',(2,-6,.25),.5),('zero_dt',(7,8,0),7.0)]:
    equals('02.4',n,'advance',inputs,e)
for n,inputs in [('negative_dt',(1,1,-1)),('nan',(1,1,float('nan'))),
                 ('inf_velocity',(1,float('inf'),1)),('overflow',(1e308,1e308,2))]:
    rejects('02.4',n,'advance',inputs)
def pure_advance(t,m):
    output=io.StringIO()
    with redirect_stdout(output):
        m.advance(1,2,.5)
    t.assertEqual(output.getvalue(),'')
add('02.4','no_printing',pure_advance)
UNITS=[{'id':1,'name':'Scout','health':5},{'id':2,'name':'Guard','health':0}]
equals('03.1','index','index_units',(UNITS,),{1:UNITS[0],2:UNITS[1]})
equals('03.1','living','living_units',(UNITS,),[UNITS[0]])
equals('03.1','empty','living_units',([],),[])
rejects('03.1','duplicate','index_units',([UNITS[0],UNITS[0]],))
def independent_records(t,m):
    original=[dict(x) for x in UNITS]
    result=m.living_units(original)
    result[0]['name']='Changed'
    t.assertEqual(original[0]['name'],'Scout')
add('03.1','record_copy',independent_records)
for n,inputs,e in [('normal',(8,5),3),('exact',(5,5),0),('poor',(4,5),4),('free',(4,0),4)]:
    equals('03.2',n,'spend',inputs,e)
for n,inputs in [('negative_cost',(4,-1)),('negative_balance',(-1,2)),('bool',(True,2))]:
    rejects('03.2',n,'spend',inputs)
def import_no_side_effect(t,m):
    stream=io.StringIO()
    with redirect_stdout(stream):
        importlib.reload(m)
    t.assertEqual(stream.getvalue(),'')
add('03.2','import_no_output',import_no_side_effect)
SAVE={'version':1,'x':2,'health':90}
def roundtrip(t,m):
    t.assertEqual(m.decode_save(m.encode_save(SAVE)),SAVE)
add('03.3','roundtrip',roundtrip)
for n,text in [('missing','{"version":1,"x":2}'),
 ('bad_type','{"version":1,"x":"2","health":90}'),
 ('version','{"version":2,"x":2,"health":90}'),
 ('truncated','{"version":'),('bool','{"version":true,"x":2,"health":90}'),
 ('range','{"version":1,"x":2,"health":101}'),
 ('extra','{"version":1,"x":2,"health":90,"cheat":1}'),
 ('duplicate','{"version":1,"x":2,"x":3,"health":90}'),
 ('too_large',' '*10001),('wrong_root','[]')]:
    rejects('03.3',n,'decode_save',(text,))
def failed_load_keeps_state(t,m):
    old=dict(SAVE)
    current=dict(old)
    try:
        current=m.decode_save('{broken')
    except ValueError:
        pass
    t.assertEqual(current,old)
add('03.3','failed_load_keeps_state',failed_load_keeps_state)
for s,event,e in [('idle','move','moving'),('moving','stop','idle'),
 ('idle','hit','stunned'),('moving','hit','stunned'),('stunned','recover','idle'),
 ('stunned','move','stunned'),('idle','stop','idle'),('moving','recover','moving')]:
    equals('03.4',s+'_'+event,'transition',(s,event),e)
rejects('03.4','unknown_state','transition',('flying','move'))
for n,inputs,e in [('single',(10,3),7),('lethal',(2,5),0),('zero',(10,0),10),('dead',(0,4),0)]:
    equals('04.1',n,'apply_damage',inputs,e)
rejects('04.1','negative_damage','apply_damage',(10,-1))
rejects('04.1','negative_health','apply_damage',(-1,2))
for n,inputs,e in [('inside',(2,1,4),3),('right',(3,1,4),3),('left',(0,-1,4),0),('wait',(1,0,4),1)]:
    equals('04.2',n,'bounded_move',inputs,e)
rejects('04.2','bad_size','bounded_move',(0,1,0))
def movement_property(t,m):
    for size in range(1,9):
        for p in range(size):
            for delta in (-2,-1,0,1,2):
                result=m.bounded_move(p,delta,size)
                t.assertTrue(0<=result<size)
                t.assertIn(result,(p,p+delta))
add('04.2','bounds_property_180_inputs',movement_property)
equals('05.1','normalise','normalise_command',(' D ',),'d')
for n,p,c,e in [('right',(0,0),'d',(1,0)),('edge',(0,0),'a',(0,0)),
 ('unknown',(2,2),'launch',(2,2)),('upper',(2,2),' W ',(2,1))]:
    equals('05.1',n,'step_position',(p,c),e)
equals('05.1','render','render_grid',((1,0),3),'.P.\n...\n..E')
def redraw(t,m):
    p=(2,2)
    before=p
    t.assertEqual(m.render_grid(p,3),m.render_grid(p,3))
    t.assertEqual(p,before)
add('05.1','redraw_no_movement',redraw)
for n,state,c,e in [
 ('move',{'x':0,'y':0,'won':False},'d',{'x':1,'y':0,'won':False}),
 ('wall',{'x':1,'y':0,'won':False},'s',{'x':1,'y':0,'won':False}),
 ('left',{'x':0,'y':0,'won':False},'a',{'x':0,'y':0,'won':False}),
 ('top',{'x':0,'y':0,'won':False},'w',{'x':0,'y':0,'won':False}),
 ('right',{'x':9,'y':0,'won':False},'d',{'x':9,'y':0,'won':False}),
 ('bottom',{'x':0,'y':9,'won':False},'s',{'x':0,'y':9,'won':False}),
 ('win',{'x':9,'y':8,'won':False},'s',{'x':9,'y':9,'won':True}),
 ('after_win',{'x':9,'y':9,'won':True},'a',{'x':9,'y':9,'won':True}),
 ('invalid',{'x':0,'y':0,'won':False},'?',{'x':0,'y':0,'won':False})]:
    equals('05.2',n,'step_world',(state,c),e)
def world_not_mutated(t,m):
    state={'x':0,'y':0,'won':False}
    new=m.step_world(state,'d')
    t.assertEqual(state,{'x':0,'y':0,'won':False})
    t.assertIsNot(new,state)
add('05.2','no_mutation',world_not_mutated)
equals('05.3','empty','replay',([],),{'x':0,'y':0,'won':False})
equals('05.3','winning','replay',(['d']*9+['s']*9,),{'x':9,'y':9,'won':True})
def same_replay(t,m):
    commands=['d']*9+['s']*9+['?','a']
    t.assertEqual(m.replay(commands),m.replay(commands))
add('05.3','same_inputs',same_replay)
def digest_order(t,m):
    a={'x':1,'y':2,'won':False}
    b={'won':False,'y':2,'x':1}
    t.assertEqual(m.state_digest(a),m.state_digest(b))
    t.assertEqual(len(m.state_digest(a)),64)
add('05.3','canonical_digest',digest_order)

if not COUNTS:
    parser.error('No automated lab for that lesson. See the evidence-based lab worksheet.')
print('Checking ' + ('REFERENCE solutions' if args.reference else 'STUDENT work'))
print('Contract checks by lesson: ' + json.dumps(COUNTS,sort_keys=True))
suite=unittest.defaultTestLoader.loadTestsFromTestCase(Contracts)
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
