import random,unittest
from reference.python.g16 import Machine,assemble,AssemblyError,ExecutionLimit,sext
from reference.python.cpu_cases import CASES

class G16Tests(unittest.TestCase):
    def test_hand_encoded_example(self):
        program=assemble('LDI r1,5\nLDI r2,7\nADD r3,r1,r2\nST r3,r0,3\nLD r4,r0,3\nHALT')
        self.assertEqual(program,[0x1205,0x1407,0x2650,0x5603,0x4803,0xf000])
        m=Machine(program);trace=m.run();self.assertEqual(m.memory[3],12);self.assertEqual(m.regs[4],12)
        self.assertEqual(len(trace),6);self.assertEqual(trace[-1].halt,1)
    def test_branch_label_encoding(self):
        self.assertEqual(assemble('start: NOP\nBZ r0,start\nHALT'),[0,0x61fe,0xf000])
    def test_trace_side_effect_masking(self):
        m=Machine(assemble('LDI r0,3\nNOP\nHALT'));trace=m.run()
        for t in trace:self.assertEqual((t.reg_we,t.rd,t.reg_value,t.mem_we,t.mem_addr,t.mem_value),(0,0,0,0,0,0))
    def test_halt_retires_once(self):
        m=Machine([0xf000]);self.assertIsNotNone(m.step());self.assertIsNone(m.step());self.assertEqual(m.retired,1)
    def test_fault_is_not_retired(self):
        m=Machine([0x8000]);self.assertEqual(m.run(),[]);self.assertEqual(m.pc,0)
    def test_fetch_255_then_fault(self):
        m=Machine([0]*256);m.pc=255;t=m.step();self.assertEqual(t.next_pc,256)
        self.assertIsNone(m.step());self.assertEqual(m.fault,'fetch_address')
    def test_signed_extension(self):
        self.assertEqual(sext(511,9),-1);self.assertEqual(sext(256,9),-256);self.assertEqual(sext(31,6),31)
    def test_invalid_assembly(self):
        for source in ('LDI r1,256','LDI r8,0','ST r1,r2,32','JMP 256','BZ r1,missing','NOP 1','x:NOP\nx:HALT','.word -1'):
            with self.subTest(source=source),self.assertRaises(AssemblyError):assemble(source)
    def test_execution_budget(self):
        with self.assertRaises(ExecutionLimit):Machine(assemble('JMP 0')).run(10)
    def test_seeded_random_arithmetic(self):
        rng=random.Random(7344)
        for case in range(100):
            regs=[0]*8;source=[]
            for _ in range(100):
                dst=rng.randrange(8)
                if rng.randrange(3)==0:
                    value=rng.randrange(-256,256);source.append(f'LDI r{dst},{value}')
                    if dst:regs[dst]=value&65535
                else:
                    a,b=rng.randrange(8),rng.randrange(8);op=rng.choice(['ADD','SUB'])
                    source.append(f'{op} r{dst},r{a},r{b}')
                    value=(regs[a]+regs[b] if op=='ADD' else regs[a]-regs[b])&65535
                    if dst:regs[dst]=value
            source.append('HALT');m=Machine(assemble('\n'.join(source)));m.run()
            self.assertEqual(m.regs,regs,f'case={case}, seed=7344')

def case_test(case):
    def test(self):
        m=Machine(assemble(case.source));trace=m.run()
        self.assertEqual(m.fault,case.fault)
        for reg,value in case.registers.items():self.assertEqual(m.regs[reg],value)
        for addr,value in case.memory.items():self.assertEqual(m.memory[addr],value)
        self.assertEqual(m.regs[0],0)
        self.assertTrue(all(t.index==i for i,t in enumerate(trace)))
    return test
for case in CASES:setattr(G16Tests,'test_directed_'+case.name,case_test(case))
if __name__=='__main__':unittest.main()
