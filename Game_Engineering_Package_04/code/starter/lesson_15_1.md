# Student contract 15.1: Language paradigms and type systems

Write one rule in imperative and pure-functional styles, then define a small typed C-compatible interface for a mock subsystem. Pass: state allocation ownership and reject type-invalid expressions in a toy checker.

1. Implement the same bounded damage rule in imperative and pure-functional styles and compare a full input table.
2. Implement Number/Boolean type rules for arithmetic and logical operators.
3. Write a C-compatible header with explicit ownership, null and error policies.
4. Use the later C bridge to compile an actual C implementation and call it through a C++ wrapper.

## Cases

1. damage below armor -> zero effective damage
2. damage exceeds remaining HP -> clamp at zero
3. negative domain input rejected
4. Number+Number accepted
5. Number+Boolean rejected
6. null output rejected without dereference

## Evidence

Two equivalent rule implementations, type-rule table, invalid-expression tests and a documented C boundary.

## Transfer

A damage function reads a global random generator. Redesign its interface so a test can reproduce the same result without relying on global state.
