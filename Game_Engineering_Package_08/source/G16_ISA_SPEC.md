# G16 v1 instruction-set and execution contract
## Scope and identity
G16 v1 is an original teaching ISA authored for this package. It is **not RISC-V**, not a commercial processor and not a full-ISA compliance claim. The RISC-V material remains assigned comparative reading about the distinction between architecture and implementation. Do not use a RISC-V compiler's machine code as G16 input. [R35]

The reference Python interpreter and single-cycle RTL implement this bounded contract. The learner must still build or modify an implementation, independently verify it, and complete the pipeline and variable-latency-memory work required by the lessons. The reference's combinational memory ports do not model synchronous FPGA block RAM.

## Architectural state
Eight registers hold unsigned 16-bit bit patterns. Arithmetic interprets them modulo 65536 unless an instruction explicitly sign-extends an immediate. Register r0 always reads zero and discards register writes; it does not suppress address checks or instruction faults.

The PC is a 16-bit **word address**. Code contains 256 separate 16-bit words at addresses 0 through 255. Data contains another 256 words at addresses 0 through 255. Instruction and data spaces are separate, so a data store cannot modify code in this baseline. An image shorter than 256 words is padded with NOP words by the vector writer. The execution budget prevents an unintended NOP stream from running forever.

Reset sets PC, registers, stopped state and retirement count to zero. The core itself does not own the external data RAM; the reference testbench initializes RAM to zero for each test. A system-level reset policy for external memory must be specified separately. Reset suppresses retirement and writes.

## Instruction encodings
Bits are numbered 15 down to 0. Fields are integers, not textual register names.

| Instruction | Opcode and fields | Semantics |
|---|---|---|
| NOP | Exactly 0x0000 | No side effects; PC := PC+1 |
| LDI rd, imm9 | op=1; rd[11:9]; imm[8:0] | Sign-extend imm9 to 16 bits; write rd |
| ADD rd, ra, rb | op=2; rd[11:9]; ra[8:6]; rb[5:3]; low[2:0]=0 | rd := (ra+rb) mod 65536 |
| SUB rd, ra, rb | op=3; same register fields and reserved bits | rd := (ra-rb) mod 65536 |
| LD rd, base, off6 | op=4; rd[11:9]; base[8:6]; off[5:0] | Load data at validated effective address |
| ST src, base, off6 | op=5; src[11:9]; base[8:6]; off[5:0] | Store src at validated effective address |
| BZ reg, disp9 | op=6; test register[11:9]; disp[8:0] | If register is zero, PC := PC+1+sext(disp9) |
| JMP address8 | op=7; reserved[11:8]=0; target[7:0] | PC := unsigned absolute word target |
| HALT | Exactly 0xF000 | Retire once; PC := PC+1; stop |

Immediate ranges are -256 through 255 for signed nine-bit values and -32 through 31 for signed six-bit values. Branch targets and sequential PC updates wrap to 16 bits; an out-of-range fetch faults on the next attempted fetch. Effective address is `(base + sign_extend(off6)) & 0xFFFF`; the result must then be in 0..255. A wrapped result of zero is legal. There are no byte enables, unaligned accesses, privilege levels, interrupts or address translation in this baseline.

## Faults are not retirements
The following terminate execution without retiring the faulting instruction: an instruction fetch outside code addresses 0..255; a data address outside 0..255; or an illegal encoding. Illegal encodings include opcodes 8 through E, nonzero low bits in NOP, nonzero reserved low three bits in ADD/SUB, nonzero reserved JMP bits, and any opcode-F word other than F000.

On a fault, the PC remains at the faulting instruction or invalid fetch address, and no register or data-memory side effect from that instruction occurs. Previously retired effects remain. In particular, `LD r0` with an invalid address faults even though the destination is the constant-zero register. Error priority in the reference is fetch address first, then instruction decode, then data address for valid memory opcodes.

The RTL terminal fault codes are 1=fetch address, 2=illegal instruction, 3=data address. Code zero means no fault. A terminal status must be compared separately from the retirement stream so that a prematurely stopped design cannot pass by emitting an empty trace.

## Retirement trace schema
Each accepted architectural instruction emits exactly one row. Fields are decimal integers in CSV order:

```text
index,pc,instr,next_pc,reg_we,rd,reg_value,
mem_we,mem_addr,mem_value,halt
```

`index` begins at zero. Register-write fields are enabled only for a real write to r1..r7. Disabled register fields use zero for rd and value. Store fields are enabled only for a committed store; disabled memory address and value are zero. Loads are represented through the register-write result, not a memory-write event. HALT emits `halt=1` once. NOP still retires.

Comparing equal retirement indices is necessary but not sufficient: compare every enabled effect, terminal fault, final PC, all registers and final data RAM. A stalled or pipelined implementation may take a different number of cycles. It may not reorder committed effects under this simple in-order contract.

## Worked program and independent encoding
```text
LDI r1, 5       ; 1205
LDI r2, 7       ; 1407
ADD r3, r1, r2  ; 2650
ST  r3, r0, 3   ; 5603
LD  r4, r0, 3   ; 4803
HALT            ; F000
```

After six retirements, r3=12, r4=12 and data[3]=12. PC=6, stopped=true and fault is absent. For ADD, 0x2000+(3<<9)+(1<<6)+(2<<3)=0x2650. This hand calculation is independent of the assembler's field-composition code.

## Assembly syntax and limitations
The included two-pass assembler accepts case-insensitive operation/register names, comma-separated or whitespace-separated operands, semicolon or hash comments and case-sensitive labels. A label refers to a word address. `BZ r1, label` computes displacement from PC+1; a numeric BZ operand is already a signed relative displacement. `JMP label` uses an absolute word address. A `.word` directive admits a 16-bit literal for deliberate illegal-instruction tests.

Duplicate/invalid labels, invalid registers, out-of-range immediates, unknown mnemonics, wrong operand counts and images exceeding 256 words are errors. There is no linker, C calling convention, stack convention, binary executable format or operating-system ABI. A supported assembled program satisfies the course's compiled-or-assembled requirement; claiming a general compiler toolchain would require additional work.

## Baseline and extension evidence
`reference/python/cpu_cases.py` defines 32 directed case specifications. `tests/test_g16.py` checks those plus independent hand encoding, fault non-retirement, signed extension, execution limits and 100 seeded random arithmetic programs. The HDL comparison vector generator writes 32 directed plus 20 random cases with seed 7344. Those expected files are software output until an actual RTL comparison runs.

The provided HDL runner compiles the simple core with Icarus, compares retirement CSVs, then checks terminal PC, faults, registers and all data memory. That runner was not executed in the authoring environment. Its presence is not evidence of a passing RTL core.

For the pipeline extension, choose and document stage boundaries, valid bits, forwarding paths, load-use stall rules and branch-resolution timing. For variable-latency memory, define request and response acceptance and preserve a request's payload until acceptance. Integrate the protocol without replaying accepted stores. Report baseline and extended implementations separately.
