import unittest
from gradlab.systems import *

class SystemsTests(unittest.TestCase):
    def test_scalar(self):
        x,lam=xpbd_scalar(.1,0,1,.01,.1)
        self.assertAlmostEqual(x,.05); self.assertAlmostEqual(lam,-.05)
    def test_scalar_stationarity(self):
        x,lam=xpbd_scalar(.1,0,1,.01,.1)
        y,lam2=xpbd_scalar(x,0,1,.01,.1,lam)
        self.assertAlmostEqual(y,x); self.assertAlmostEqual(lam2,lam)
    def test_bar_vs_dense(self):
        u=[0,.1,-.05,.02]; v=[0,0,0,0]
        a,_=bar_step(u,v,dt=.01,compliance=.001,iterations=100)
        b,_=bar_step(u,v,dt=.01,compliance=.001,method='implicit')
        self.assertLess(max(abs(x-y) for x,y in zip(a,b)),1e-10)
    def test_bar_pin_and_duration(self):
        a=simulate_bar(duration=.1)
        self.assertEqual(a['u'][0],0); self.assertAlmostEqual(a['duration'],.1)
    def test_stream_budget(self):
        s=StreamModel(10,3)
        self.assertEqual(s.request(Request('a',7,1,0)),'accepted'); s.tick()
        self.assertEqual(s.request(Request('b',8,2,0)),'accepted'); s.tick()
        self.assertLessEqual(s.peak,10); self.assertNotIn('a',s.resident)
    def test_stream_backpressure(self):
        s=StreamModel(10,1); s.request(Request('a',7,1,0))
        self.assertEqual(s.request(Request('b',7,1,0)),'backpressure')
        self.assertEqual(s.request(Request('big',11,1,0)),'oversize')
    def test_teleport(self):
        s=StreamModel(10,1); s.request(Request('a',7,1,0)); s.teleport()
        self.assertIsNone(s.tick()); self.assertEqual(s.request(Request('b',3,1,0)),'stale')
    def test_stale_authority(self):
        s=FencedStore(); s.grant('B',1)
        self.assertEqual(s.commit('A',0,'reward',1),'stale')
        self.assertEqual(s.commit('B',1,'reward',1),'committed')
    def test_idempotency_conflict(self):
        s=FencedStore(); s.commit('A',0,'r',1)
        self.assertEqual(s.commit('A',0,'r',1),'duplicate')
        self.assertEqual(s.commit('A',0,'r',2),'conflict')
    def test_dedup_capacity(self):
        s=FencedStore(1); s.commit('A',0,'r',1)
        self.assertEqual(s.commit('A',0,'s',1),'backpressure')
    def test_model_safe(self): self.assertTrue(lifecycle_check()['safe'])
    def test_model_counterexample(self):
        r=lifecycle_check(True)
        self.assertFalse(r['safe']); self.assertEqual(r['counterexample'],['request','release','complete'])
    def test_replay_canonical(self): self.assertEqual(replay_hash([{'a':1,'b':2}]),replay_hash([{'b':2,'a':1}]))
