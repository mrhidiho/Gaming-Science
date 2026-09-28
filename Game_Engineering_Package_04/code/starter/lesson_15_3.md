# Student contract 15.3: Bytecode, virtual machines and bounded execution

Compile the expression language into stack bytecode and compare results to the tree evaluator. Pass: reject stack underflow, invalid opcodes and over-budget execution; preserve source context for errors.

1. Specify each opcode, stack effect, operand order and error location.
2. Compile the AST in postorder and compare golden stack traces.
3. Implement VM checks for malformed instructions and resource limits.
4. Differentially test valid expressions and error behavior, explicitly documenting shared validation code.

## Cases

1. 8-3*2 -> 2
2. five instructions pass with fuel 5, fail with 4
3. ADD on empty -> underflow
4. unknown opcode rejected
5. two final values rejected
6. PUSH beyond stack cap rejected
7. invalid literal and arithmetic range rejected

## Evidence

Opcode table, stack traces, compiler/VM differential tests, malformed-bytecode tests and limit matrix.

## Transfer

Add a conditional jump. Identify the new obligations for instruction-pointer validation, fuel, reachable stack states and source-level termination claims.
