import math,random,unittest
from itertools import product
from fractions import Fraction
from reference.python.circuits import *
from reference.python.digital import *
from reference.python.fixed_point import *
from reference.python.fifo import SyncFIFO
from reference.python.peripherals import Timer,Buffer,set_wins_pending
from reference.python.memory_protocol import Memory,Request
from reference.python.video import Raster,rgb,write_ppm
from pathlib import Path
import tempfile

class CircuitTests(unittest.TestCase):
    def test_divider(self):
        x=divider(5,2000,3000);self.assertAlmostEqual(x.voltage,3);self.assertAlmostEqual(x.source_current,.001)
    def test_loaded_divider(self):
        x=divider(5,2000,3000,6000)
        self.assertAlmostEqual(x.voltage,2.5);self.assertAlmostEqual(x.source_current,.00125)
        self.assertAlmostEqual(x.bottom_current,2.5/3000);self.assertAlmostEqual(x.load_current,2.5/6000)
    def test_power_and_kcl(self):
        for load in (None,1,3000,6000,12000,1e7):
            x=divider(5,2000,3000,load)
            self.assertLess(abs(x.kcl_residual),1e-12);self.assertAlmostEqual(x.source_power,x.resistor_power,14)
    def test_tolerance(self):
        lo,hi=divider_bounds(5,2000,3000,.01)
        self.assertAlmostEqual(lo,5*2970/4990);self.assertAlmostEqual(hi,5*3030/5010)
    def test_rc(self):
        self.assertAlmostEqual(rc_step(.01,10000,1e-6,3.3),3.3*(1-math.exp(-1)))
        self.assertAlmostEqual(rc_step(0,10000,1e-6,3.3,1),1)
    def test_rc_cutoff(self):
        mag,phase=rc_response(1/(2*math.pi*.01),10000,1e-6)
        self.assertAlmostEqual(mag,1/math.sqrt(2));self.assertAlmostEqual(phase,-math.pi/4)
    def test_euler_converges_and_can_diverge(self):
        errors=[abs(rc_euler(n,.01/n,10000,1e-6,1)[-1]-(1-math.exp(-1))) for n in(10,100,1000)]
        self.assertGreater(errors[0],errors[1]);self.assertGreater(errors[1],errors[2])
        self.assertGreater(abs(rc_euler(10,.03,10000,1e-6,1)[-1]-1),100)
    def test_hysteresis(self):
        h=Hysteresis();self.assertEqual([h.update(x) for x in[1.4,1.6,1.7,1.81,1.7,1.6,1.49]],[0,0,0,1,1,1,0])
        self.assertEqual(h.update(1.8),1);self.assertEqual(h.update(1.5),0)
    def test_quantizer_edges(self):
        self.assertEqual(quantize(-1),0);self.assertEqual(quantize(3.3),4095)
        self.assertEqual(quantize(1.65),2048);self.assertEqual(quantize(9),4095)
    def test_quantizer_error(self):
        for k in range(4096):
            v=reconstruct(k);self.assertEqual(quantize(v),k)
            self.assertLessEqual(abs(v-k*3.3/4096),3.3/8192+1e-15)
    def test_alias_and_filter(self):
        for n in range(100):self.assertAlmostEqual(math.cos(2*math.pi*700*n/1000),math.cos(2*math.pi*300*n/1000),11)
        y=lowpass([1]*9,.25);self.assertLess(y[7],.9);self.assertGreaterEqual(y[8],.9)
    def test_reject_bad_inputs(self):
        for fn,args in[(divider,(5,0,100)),(quantize,(1,0)),(rc_step,(-1,1,1,1)),(Hysteresis,(2,1)),(lowpass,([1],0))]:
            with self.assertRaises(ValueError):fn(*args)

class DigitalTests(unittest.TestCase):
    def test_exhaustive_adder(self):
        for a,b,c in product(range(16),range(16),range(2)):
            s,carry=ripple_add(a,b,c);self.assertEqual(s+16*carry,a+b+c)
    def test_mux_and_decoder(self):
        self.assertEqual(mux(4,9,0),4);self.assertEqual(mux(4,9,1),9)
        for i in range(8):self.assertEqual(decoder(i,3),2**i)
    def test_fsm_exhaustive(self):
        for state in State:
            for bits in product((False,True),repeat=5):
                reset,abort,start,complete,ack=bits
                expected=State.IDLE if reset or abort else {State.IDLE:(State.RUN if start else State.IDLE),State.RUN:(State.DONE if complete else State.RUN),State.DONE:(State.IDLE if ack else State.DONE)}[state]
                self.assertEqual(next_state(state,reset=reset,abort=abort,start=start,complete=complete,acknowledge=ack),expected)
        self.assertEqual(next_state(9),State.IDLE)
    def test_timing(self):
        self.assertAlmostEqual(setup_budget(.8,5.6,.6,.5),7.5)
        self.assertAlmostEqual(hold_slack(.1,.05,.2,.05),-.1)
    def test_wrap_and_saturation(self):
        self.assertEqual(wrap_signed(140,8),-116);self.assertEqual(saturate(140,8),127)
        self.assertEqual(wrap_signed(-140,8),116);self.assertEqual(saturate(-140,8),-128)
    def test_rounding_ties(self):
        self.assertEqual([round_shift_even(x,2) for x in[6,10,-6,-10]],[2,2,-2,-2])
    def test_rounding_exhaustive(self):
        for shift in range(1,7):
            for n in range(-1000,1001):self.assertEqual(round_shift_even(n,shift),round(Fraction(n,1<<shift)))
    def test_multiply(self):self.assertEqual(fixed_multiply(384,-192),-288)
    def test_saturating_adder(self):
        for a,b in product(range(-128,128),repeat=2):self.assertEqual(sat_add(a,b,8),max(-128,min(127,a+b)))
    def test_fifo_boundaries(self):
        q=SyncFIFO(1);c=q.step(True,11,True);self.assertTrue(c.push);self.assertFalse(c.pop)
        c=q.step(True,22,True);self.assertFalse(c.push);self.assertTrue(c.pop);self.assertEqual(c.out_data,11)
        self.assertEqual(len(q.queue),0)
    def test_fifo_random_scoreboard(self):
        for depth in(1,3,8):
            q=SyncFIFO(depth,16);gold=[];rng=random.Random(731+depth)
            for _ in range(5000):
                valid=bool(rng.getrandbits(1));data=rng.randrange(65536);ready=bool(rng.getrandbits(1));reset=rng.randrange(113)==0
                old=list(gold);c=q.step(valid,data,ready,reset)
                if reset:gold=[];self.assertFalse(c.push or c.pop)
                else:
                    self.assertEqual(c.in_ready,len(old)<depth);self.assertEqual(c.out_valid,bool(old))
                    if old:self.assertEqual(c.out_data,old[0])
                    if ready and old:gold.pop(0)
                    if valid and len(old)<depth:gold.append(data)
                self.assertEqual(list(q.queue),gold)
    def test_fifo_stability_and_reset(self):
        q=SyncFIFO(3);q.step(True,21);q.step(True,22)
        for _ in range(5):self.assertEqual(q.step().out_data,21)
        self.assertEqual(q.step(True,99,True,True).count_after,0)

class IntegrationModelTests(unittest.TestCase):
    def test_timer_edge_and_set_wins(self):
        t=Timer(width=4)
        self.assertFalse(t.tick(enable=True,compare=3)['event']);self.assertFalse(t.tick(enable=True,compare=3)['event'])
        result=t.tick(enable=True,compare=3,clear=True);self.assertTrue(result['event']);self.assertTrue(result['pending'])
        self.assertFalse(t.tick(enable=False,compare=3,clear=True)['pending'])
    def test_timer_wrap_and_disable(self):
        t=Timer(width=2,count=3);self.assertTrue(t.tick(enable=True,compare=0,irq_enable=False)['pending'])
        self.assertFalse(t.tick(enable=False,compare=0,irq_enable=False)['irq'])
        self.assertEqual(t.tick(enable=False,compare=0,reset=True)['count'],0)
    def test_buffer_ownership(self):
        b=Buffer();token=b.submit()
        with self.assertRaises(RuntimeError):b.cpu_write()
        with self.assertRaises(RuntimeError):b.complete(token+1)
        b.complete(token);b.cpu_write()
        with self.assertRaises(RuntimeError):b.complete(token)
    def test_memory_single_accept(self):
        m=Memory();req=Request(True,3,99)
        self.assertTrue(m.step(req,latency=3).accepted_request)
        for _ in range(2):self.assertFalse(m.step(req,response_ready=False).accepted_request)
        e=m.step(req,response_ready=False);self.assertTrue(e.response_valid)
        self.assertEqual(m.write_count,1);self.assertEqual(m.words[3],99)
        self.assertTrue(m.step(None).accepted_response);self.assertEqual(m.write_count,1)
    def test_memory_error_and_reset(self):
        m=Memory();m.step(Request(True,256,8));e=m.step();self.assertTrue(e.response.error);self.assertEqual(m.write_count,0)
        m.step(Request(True,7,11),latency=3);m.step(reset=True)
        self.assertEqual(m.words[7],11);self.assertIsNone(m.response)
    def test_memory_response_stable(self):
        m=Memory();m.words[5]=123;m.step(Request(False,5))
        values=[m.step(response_ready=False).response for _ in range(5)]
        self.assertTrue(all(x==values[0] for x in values));self.assertEqual(values[0].data,123)
    def test_raster_exact_geometry(self):
        r=Raster();pixels=[r.step() for _ in range(80*60)]
        self.assertEqual(sum(p.active for p in pixels),64*48);self.assertEqual(sum(p.frame_start for p in pixels),1)
        self.assertEqual((r.x,r.y),(0,0));self.assertEqual((pixels[-1].x,pixels[-1].y),(79,59))
    def test_reference_image(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'f.ppm';write_ppm(p);raw=p.read_bytes();head=b'P6\n64 48\n255\n'
            self.assertTrue(raw.startswith(head));self.assertEqual(len(raw)-len(head),64*48*3)
        self.assertEqual(rgb(20,16),(255,128,0))
if __name__=='__main__':unittest.main()
