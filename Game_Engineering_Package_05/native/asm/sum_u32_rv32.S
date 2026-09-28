# Hand-authored RV32I teaching routine, ILP32 integer calling convention.
# Input a0: aligned pointer to n readable uint32 words; a1: n.
# Output a0: sum modulo 2^32. Caller provides valid memory and stack.
# ra save is deliberately redundant for this leaf; useful for frame annotation.
.text
.globl course_sum_u32
course_sum_u32:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw s0, 8(sp)
    addi s0, zero, 0
    beq a1, zero, .Ldone
.Lloop:
    lw t0, 0(a0)
    add s0, s0, t0
    addi a0, a0, 4
    addi a1, a1, -1
    bne a1, zero, .Lloop
.Ldone:
    addi a0, s0, 0
    lw s0, 8(sp)
    lw ra, 12(sp)
    addi sp, sp, 16
    jalr zero, 0(ra)
