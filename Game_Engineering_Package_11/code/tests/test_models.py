import math,unittest
from itertools import product
from reference.coherence import MSI
from reference.scheduler import Instruction,schedule,example_program
from reference.cache import Cache,CacheConfig,serial_cycles
from reference.models import inverter_chain,dynamic_power,energy_per_item
from reference.protocol import Mailbox,run_mailbox,queue_step,explore_queue
from reference.ecc import parity,fault_campaign
from reference.analysis import quantile,paired_bootstrap
from reference.security import Controller


class CoherenceTests(unittest.TestCase):
    def test_worked_trace(self):
        m=MSI(); reads=[]
        for c,op,v in [(0,'R',0),(1,'R',0),(0,'W',7),(1,'R',0),(1,'W',9),(0,'R',0)]:
            out=m.request(c,op,v)
            if op=='R':reads.append(out)
        self.assertEqual(reads,[0,0,7,9]);self.assertEqual(m.state,['S','S']);self.assertEqual(m.memory,9)
    def test_exhaustive_atomic_traces(self):
        actions=[(c,op,v) for c in (0,1) for op,v in [('R',0),('W',0),('W',1)]]
        for trace in product(actions,repeat=6):
            m=MSI();oracle=0
            for c,op,v in trace:
                out=m.request(c,op,v)
                if op=='W':oracle=v
                else:self.assertEqual(out,oracle)
    def test_invalid_core(self):
        with self.assertRaises(ValueError):MSI().request(2,'R')
    def test_multiple_owners_detected(self):
        with self.assertRaises(AssertionError):MSI(state=['M','M'],value=[0,0]).check()
    def test_stale_shared_detected(self):
        with self.assertRaises(AssertionError):MSI(state=['S','S'],value=[0,1]).check()


class SchedulerTests(unittest.TestCase):
    def test_example_equivalence(self):
        a=schedule(example_program(),out_of_order=False);b=schedule(example_program())
        self.assertEqual(a['committed'],b['committed']);self.assertEqual(a['committed'],dict(A=2,B=5,C=5,D=12))
    def test_example_cycles(self):
        self.assertEqual(schedule(example_program())['last_retirement_cycle'],7)
        self.assertEqual(schedule(example_program(),out_of_order=False)['last_retirement_cycle'],7)
    def test_ooo_issues_independent_early(self):
        self.assertEqual(schedule(example_program())['events']['C']['issue'],1)
        self.assertEqual(schedule(example_program(),out_of_order=False)['events']['C']['issue'],5)
    def test_precise_fault(self):
        p=example_program();p[1]=Instruction('B',('A',),3,1,True)
        r=schedule(p);self.assertEqual(r['committed'],{'A':2});self.assertEqual(r['fault'],'B')
        self.assertIn('C',r['events']);self.assertNotIn('retire',r['events']['C'])
    def test_window_one(self):
        p=example_program()
        self.assertEqual(schedule(p,window=1)['events'],schedule(p,window=1,out_of_order=False)['events'])
    def test_chain_no_overlap_advantage(self):
        p=[Instruction(str(i),(str(i-1),) if i else (),1,3) for i in range(10)]
        self.assertEqual(schedule(p,width=2)['last_retirement_cycle'],schedule(p,width=2,out_of_order=False)['last_retirement_cycle'])
    def test_long_independent_work_improves(self):
        p=[Instruction('A',(),1,10),Instruction('B',('A',),1,1),Instruction('C',(),2,10)]
        self.assertLess(schedule(p)['last_retirement_cycle'],schedule(p,out_of_order=False)['last_retirement_cycle'])
    def test_invalid_dependency(self):
        with self.assertRaises(ValueError):schedule([Instruction('A',('B',))])
    def test_invalid_latency(self):
        with self.assertRaises(ValueError):schedule([Instruction('A',latency=0)])
    def test_duplicate_name(self):
        with self.assertRaises(ValueError):schedule([Instruction('A'),Instruction('A')])
    def test_empty(self):self.assertEqual(schedule([])['committed'],{})


class ArithmeticTests(unittest.TestCase):
    def test_serial_cost(self):self.assertEqual(serial_cycles(100,10,2,30),500)
    def test_cost_invalid(self):
        with self.assertRaises(ValueError):serial_cycles(1,2,1,1)
    def test_warmup_state_retained(self):
        c=Cache(CacheConfig(1,2));c.access(0);c.access(64)
        self.assertTrue(c.access(0));self.assertTrue(c.access(64))
    def test_chain(self):
        self.assertEqual(inverter_chain(64,3)['delay'],15)
        for actual, expected in zip(inverter_chain(64,3)['sizes'], [1,4,16]):
            self.assertAlmostEqual(actual, expected)
    def test_chain_polarity(self):
        self.assertTrue(inverter_chain(64,3)['inverting']);self.assertFalse(inverter_chain(64,4)['inverting'])
    def test_bad_chain(self):
        with self.assertRaises(ValueError):inverter_chain(0,3)
    def test_power(self):self.assertAlmostEqual(dynamic_power(.2,10e-12,1,100e6),.0002)
    def test_voltage_scaling(self):self.assertAlmostEqual(dynamic_power(.2,10e-12,.8,100e6),.000128)
    def test_energy(self):self.assertAlmostEqual(energy_per_item(.003,2e6),1.5e-9)
    def test_invalid_throughput(self):
        with self.assertRaises(ValueError):energy_per_item(.003,0)
    def test_quantile_interpolation(self):self.assertAlmostEqual(quantile([0,10],.25),2.5)
    def test_quantile_bounds(self):
        self.assertEqual(quantile([1,3],0),1);self.assertEqual(quantile([1,3],1),3)
    def test_quantile_invalid(self):
        with self.assertRaises(ValueError):quantile([], .5)
    def test_bootstrap_constant(self):
        r=paired_bootstrap([10,20,30],[8,16,24],100)
        self.assertAlmostEqual(r['lower'],1.25);self.assertAlmostEqual(r['upper'],1.25)
    def test_bootstrap_repeatable(self):
        a=paired_bootstrap([10,12,8,20],[8,9,7,18],100,7)
        b=paired_bootstrap([10,12,8,20],[8,9,7,18],100,7)
        self.assertEqual(a,b)
    def test_parity_even_double_miss(self):
        self.assertEqual(parity(0),parity(3));self.assertNotEqual(parity(0),parity(1))
    def test_campaign_counts(self):self.assertEqual(fault_campaign()['cases'],dict(clean=16,single=128,double=448))


class ProtocolTests(unittest.TestCase):
    def test_clock_ratios(self):
        for a,b in [(2,3),(3,2),(5,7),(1,1)]:
            for phase in range(min(b,3)):
                with self.subTest(a=a,b=b,phase=phase):
                    r=run_mailbox(list(range(12)),a,b,destination_phase=phase)
                    self.assertEqual(r['accepted'],r['delivered'])
    def test_backpressure(self):
        r=run_mailbox(list(range(8)),2,3,blocked_ticks=range(50))
        self.assertEqual(r['accepted'],r['delivered'])
    def test_busy_retains_payload(self):
        m=Mailbox();self.assertTrue(m.step(True,False,7)[0])
        self.assertFalse(m.step(True,False,9)[0]);self.assertEqual(m.payload,7)
    def test_coincident_edges_snapshot(self):
        m=Mailbox();m.step(True,True,7)
        self.assertEqual(m.req,1);self.assertEqual(m.req1,0)
    def test_reset_drops_undelivered(self):
        m=Mailbox();m.step(True,False,7)
        self.assertEqual(m.reset(),1);self.assertEqual(m.epoch,1);self.assertTrue(m.source_ready)
        for _ in range(10):self.assertIsNone(m.step(True,True)[1])
    def test_unilateral_reset_rejected(self):
        with self.assertRaises(ValueError):Mailbox().reset(source=True,destination=False)
    def test_stopped_destination(self):
        m=Mailbox();m.step(True,False,7)
        for _ in range(20):m.step(True,False,9)
        self.assertEqual(m.payload,7);self.assertFalse(m.source_ready)
    def test_invalid_clock(self):
        with self.assertRaises(ValueError):run_mailbox([1],0,2)
    def test_full_simultaneous_pop(self):
        q,out,push,pop=queue_step((1,2),3,True)
        self.assertEqual(q,(2,));self.assertEqual(out,1);self.assertFalse(push);self.assertTrue(pop)
    def test_empty_simultaneous_requests(self):
        q,out,push,pop=queue_step((),3,True)
        self.assertEqual(q,(3,));self.assertIsNone(out);self.assertTrue(push);self.assertFalse(pop)
    def test_queue_fixed_point(self):
        r=explore_queue();self.assertEqual(r['states'],7);self.assertTrue(r['fixed_point'])
    def test_lifo_mutation_detectable(self):
        state=(0,1);_,expected,_,_=queue_step(state,pop=True)
        self.assertNotEqual(state[-1],expected)


class SecurityTests(unittest.TestCase):
    def test_valid_completion(self):
        c=Controller();t=c.submit(0,16,7,0);self.assertEqual(t,0)
        self.assertTrue(c.complete(t,0));self.assertEqual(len(c.writes),1)
    def test_rejection_has_no_effect(self):
        c=Controller();self.assertIsNone(c.submit(4080,32,7,0));self.assertEqual(c.pending,[]);self.assertEqual(c.writes,[])
    def test_queue_limit(self):
        c=Controller(queue_limit=1);self.assertIsNotNone(c.submit(0,16,7,0));self.assertIsNone(c.submit(16,16,7,0))
    def test_stale_completion(self):
        c=Controller();t=c.submit(0,16,7,0);self.assertEqual(c.reset(),1)
        self.assertFalse(c.complete(t,0));self.assertEqual(c.writes,[])
    def test_stale_descriptor(self):
        c=Controller();c.reset();self.assertIsNone(c.submit(0,16,7,0));self.assertIsNotNone(c.submit(0,16,7,1))
    def test_duplicate_completion(self):
        c=Controller();t=c.submit(0,16,7,0);c.complete(t,0)
        self.assertFalse(c.complete(t,0));self.assertEqual(len(c.writes),1)
