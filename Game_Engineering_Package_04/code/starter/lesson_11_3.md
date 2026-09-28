# Student contract 11.3: Values, references, pointers and lifetimes

Implement functions taking values, const references and pointers with a documented null policy. Pass: explain each lifetime and identify a deliberately supplied dangling-reference example without executing undefined behavior.

1. Implement equivalent small functions taking a value, a const reference and a pointer with an explicit null policy.
2. Draw owners and borrowers for each function call. State what happens after a vector growth or owner destruction.
3. Implement a copied-value lookup and contrast it with a short-lived borrowed lookup.
4. Diagnose the supplied dangling example without executing it; submit the corrected version and reasoning.

## Cases

1. empty range -> absent
2. present ID -> copied expected position
3. missing ID -> absent
4. null optional target -> explicit result
5. copied result remains valid after source growth
6. dangling local identified by inspection

## Evidence

Parameter-choice table, lifetime diagrams, null-policy tests and a repaired invalid-reference example.

## Transfer

An event callback captures a local variable by reference and runs next frame. Show two safe designs and explain which one owns the captured state.
