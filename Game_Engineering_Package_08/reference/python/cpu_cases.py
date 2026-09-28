"""Directed specifications with independently stated architectural expectations."""
from dataclasses import dataclass,field
@dataclass(frozen=True)
class Case:
    name:str
    source:str
    registers:dict[int,int]=field(default_factory=dict)
    memory:dict[int,int]=field(default_factory=dict)
    fault:str|None=None

CASES=[
 Case('01_halt','HALT'),
 Case('02_nop','NOP\nHALT'),
 Case('03_positive_immediate','LDI r1, 255\nHALT',{1:255}),
 Case('04_negative_immediate','LDI r1, -256\nHALT',{1:65280}),
 Case('05_zero_register','LDI r0, 19\nADD r0,r0,r0\nHALT',{0:0}),
 Case('06_add','LDI r1,5\nLDI r2,7\nADD r3,r1,r2\nHALT',{3:12}),
 Case('07_subtract','LDI r1,5\nLDI r2,7\nSUB r3,r1,r2\nHALT',{3:65534}),
 Case('08_add_wrap','LDI r1,-1\nLDI r2,1\nADD r3,r1,r2\nHALT',{3:0}),
 Case('09_subtract_wrap','LDI r1,1\nSUB r3,r0,r1\nHALT',{3:65535}),
 Case('10_store_load','LDI r1,12\nST r1,r0,3\nLD r4,r0,3\nHALT',{4:12},{3:12}),
 Case('11_positive_offset','LDI r1,17\nLDI r2,10\nST r1,r2,3\nHALT',{}, {13:17}),
 Case('12_negative_offset','LDI r1,19\nLDI r2,10\nST r1,r2,-3\nLD r3,r2,-3\nHALT',{3:19},{7:19}),
 Case('13_branch_taken','BZ r0,skip\nLDI r1,99\nskip: HALT',{1:0}),
 Case('14_branch_not_taken','LDI r1,1\nBZ r1,skip\nLDI r2,7\nskip: HALT',{2:7}),
 Case('15_backward_branch','LDI r1,3\nLDI r2,1\nloop: SUB r1,r1,r2\nBZ r1,done\nBZ r0,loop\ndone: HALT',{1:0}),
 Case('16_absolute_jump','JMP done\nLDI r1,33\ndone: HALT',{1:0}),
 Case('17_register_dependency','LDI r1,4\nADD r1,r1,r1\nADD r2,r1,r1\nHALT',{1:8,2:16}),
 Case('18_store_overwrite','LDI r1,4\nST r1,r0,0\nLDI r1,9\nST r1,r0,0\nLD r2,r0,0\nHALT',{2:9},{0:9}),
 Case('19_address_255','LDI r1,255\nLDI r2,31\nST r2,r1,0\nLD r3,r1,0\nHALT',{3:31},{255:31}),
 Case('20_address_wrap','LDI r1,-1\nLDI r2,23\nST r2,r1,1\nHALT',{}, {0:23}),
 Case('21_load_zero_register','LDI r1,15\nST r1,r0,0\nLD r0,r0,0\nHALT',{0:0},{0:15}),
 Case('22_wrong_path_store','LDI r1,11\nBZ r0,done\nST r1,r0,0\ndone: HALT',{}, {0:0}),
 Case('23_illegal_opcode','.word 0x8000',fault='illegal_instruction'),
 Case('24_reserved_add','.word 0x2001',fault='illegal_instruction'),
 Case('25_reserved_nop','.word 0x0001',fault='illegal_instruction'),
 Case('26_reserved_jump','.word 0x7100',fault='illegal_instruction'),
 Case('27_reserved_halt','.word 0xf001',fault='illegal_instruction'),
 Case('28_bad_load','LDI r1,255\nLD r2,r1,1',{2:0},fault='data_address'),
 Case('29_bad_store','LDI r1,255\nLDI r2,8\nST r2,r1,1',{}, {0:0,255:0},fault='data_address'),
 Case('30_bad_load_r0','LDI r1,-1\nLD r0,r1,0',{0:0},fault='data_address'),
 Case('31_fetch_out_of_range','BZ r0,-2',fault='fetch_address'),
 Case('32_halt_no_following_effect','HALT\nLDI r1,31',{1:0}),
]
