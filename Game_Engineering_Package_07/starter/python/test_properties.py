"""Independent invariants/oracles for reference kernels. Run with Python, no deps."""
import collections
import math
import random
import unittest
from run_tests import load, equivalent

class Properties(unittest.TestCase):
    def test_broad_phase_oracle_200_scenes(self):
        rng=random.Random(261)
        solve=load('26.1')
        for _ in range(200):
            circles=[[i,rng.uniform(-5,5),rng.uniform(-5,5),rng.uniform(.02,.8)] for i in range(30)]
            out=solve({'circles':circles,'cell_size':.7})
            oracle=[]
            for i,a in enumerate(circles):
                for b in circles[i+1:]:
                    if math.hypot(a[1]-b[1],a[2]-b[2])<=a[3]+b[3]:oracle.append([a[0],b[0]])
            self.assertEqual(out['contacts'],oracle)
            self.assertTrue(set(map(tuple,oracle))<=set(map(tuple,out['candidates'])))
    def test_elastic_conservation_100_cases(self):
        rng=random.Random(262)
        for _ in range(100):
            ma,mb=rng.uniform(.2,10),rng.uniform(.2,10); va,vb=3,-2
            r=load('26.2')({'va':va,'vb':vb,'wa':1/ma,'wb':1/mb,'e':1})
            self.assertAlmostEqual(ma*va+mb*vb,ma*r['va']+mb*r['vb'])
            self.assertAlmostEqual(ma*va**2+mb*vb**2,ma*r['va']**2+mb*r['vb']**2)
    def test_sweep_time_reversal_direction(self):
        f=load('26.3')
        self.assertAlmostEqual(f({'x':0,'v':10,'lo':2,'hi':3,'dt':1}),.2)
        self.assertAlmostEqual(f({'x':0,'v':-10,'lo':-3,'hi':-2,'dt':1}),.2)
    def test_nonfinite_replay_rejected(self):
        with self.assertRaises(ValueError):load('26.4')({'left':[{'x':float('nan')}],'right':[]})
    def test_canonical_key_order(self):
        self.assertIsNone(load('26.4')({'left':[{'x':1,'y':[2]}],'right':[{'y':[2],'x':1}]}))
    def test_hierarchy_rotation(self):
        out=load('27.1')({'parents':[-1,0],'local':[[1,2,math.pi/2],[2,0,0]]})
        self.assertTrue(equivalent(out,[[1,2,math.pi/2],[1,4,math.pi/2]]))
    def test_ik_forward_reconstruction_100_cases(self):
        rng=random.Random(272)
        for _ in range(100):
            x,y=rng.uniform(-3,3),rng.uniform(-3,3)
            r=load('27.2')({'l1':2,'l2':1,'x':x,'y':y})
            a,b=r['shoulder'],r['elbow']
            self.assertTrue(equivalent(r['endpoint'],[2*math.cos(a)+math.cos(a+b),2*math.sin(a)+math.sin(a+b)]))
            if r['reachable']:self.assertTrue(equivalent(r['endpoint'],[x,y]))
    def test_audio_split_continuity(self):
        f=load('27.3');p={'sample_rate':48000,'frames':128,'frequencies':[440,880],'gains':[.2,.1]}
        first=f(p);p['phases']=first['phases'];second=f(p)
        full=f({**p,'phases':[0,0],'frames':256})
        self.assertTrue(equivalent(first['samples']+second['samples'],full['samples']))
    def test_pan_power(self):
        for i in range(21):
            r=load('27.4')({'pan':-1+i/10,'seen':[],'events':[],'min_tick':0})
            self.assertAlmostEqual(sum(v*v for v in r['gains']),1)
    def test_astar_bfs_oracle_100_maps(self):
        rng=random.Random(281);f=load('28.1')
        for _ in range(100):
            grid=[''.join('#' if rng.random()<.2 else '.' for x in range(8)) for y in range(8)]
            grid[0]='.'+grid[0][1:];grid[-1]=grid[-1][:-1]+'.'
            distance={(0,0):0};q=collections.deque([(0,0)])
            while q:
                x,y=q.popleft()
                for a,b in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    if 0<=a<8 and 0<=b<8 and grid[b][a]!='#' and (a,b) not in distance:
                        distance[a,b]=distance[x,y]+1;q.append((a,b))
            r=f({'grid':grid,'start':[0,0],'goal':[7,7],'budget':1000})
            self.assertEqual(r['status'],'found' if (7,7) in distance else 'unreachable')
            if r['status']=='found':self.assertEqual(len(r['path'])-1,distance[7,7])
    def test_search_against_exhaustive_100_trees(self):
        rng=random.Random(283);f=load('28.3')
        def minimax(t,maximum=True):
            if not isinstance(t,list):return t
            return (max if maximum else min)(minimax(c,not maximum) for c in t)
        for _ in range(100):
            tree=[[[rng.randrange(-20,21) for _ in range(3)] for _ in range(3)] for _ in range(3)]
            r=f({'tree':tree,'budget':1000,'maximizing':True})
            self.assertTrue(r['complete']);self.assertEqual(r['value'],minimax(tree))
    def test_logistic_gradient_finite_difference(self):
        f=load('28.4');w=[.1,-.2];x=[2,-1];b=.3;lr=.01
        out=f({'x':x,'w':w,'b':b,'y':1,'lr':lr})
        def loss(ww):return math.log1p(math.exp(-(sum(a*v for a,v in zip(ww,x))+b)))
        for j in range(2):
            a=w.copy();c=w.copy();a[j]+=1e-6;c[j]-=1e-6
            numeric=(loss(a)-loss(c))/2e-6
            self.assertAlmostEqual((w[j]-out['w'][j])/lr,numeric,places=6)
    def test_prediction_duplicate_once(self):
        f=load('29.1')
        p={'position':0,'ack':2,'pending':[[3,1],[3,1],[1,-1]]}
        self.assertEqual(f(p)['position'],1)
    def test_rollback_matches_full_replay_100_cases(self):
        rng=random.Random(293);f=load('29.3')
        for _ in range(100):
            tape=[rng.randrange(-1,2) for _ in range(50)];tick=rng.randrange(50);delta=rng.randrange(-1,2)
            r=f({'initial':0,'inputs':tape,'corrections':[[tick,delta]],'oldest':0})
            tape[tick]=delta;oracle=[0]
            for v in tape:oracle.append(oracle[-1]+v)
            self.assertEqual(r,oracle)
    def test_store_input_unmodified(self):
        p={'principal':'match_authority','operation':{'id':'r','player':'p','points':4},'ledger':[],'balances':{}}
        load('29.4')(p);self.assertEqual(p['ledger'],[]);self.assertEqual(p['balances'],{})
    def test_placeholder_preservation(self):
        r=load('30.2')({'text':'Hello {player_name}','bindings':{'use':'E'},'action':'use'})
        self.assertIn('{player_name}',r['text'])
    def test_mod_bool_dimension_rejected(self):
        with self.assertRaises(ValueError):load('30.3')({'version':1,'title':'x','textures':[{'name':'x','width':True,'height':2}]})

if __name__=='__main__':unittest.main(verbosity=2)
