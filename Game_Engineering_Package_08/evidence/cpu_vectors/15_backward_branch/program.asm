LDI r1,3
LDI r2,1
loop: SUB r1,r1,r2
BZ r1,done
BZ r0,loop
done: HALT
