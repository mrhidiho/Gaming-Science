# Student contract 15.4: Automata, computability and compiler optimization

Add constant folding to the toy compiler and test it against the unoptimized evaluator. Pass: include a finite-state recognizer, explain a termination restriction and document transformations deliberately excluded for semantic reasons.

1. Implement the finite-state decimal recognizer and separate lexical validity from numeric validity.
2. Add constant folding with explicit preservation of values and located runtime failures.
3. Compare original, bytecode and folded execution on golden and generated inputs.
4. Write a termination argument for the restricted language and list excluded transformations with semantic reasons.

## Cases

1. empty digits rejected; 007 accepted; 7x rejected
2. 2+3*4 folds to 14
3. (1/0)*0 retains division error
4. range overflow preserved as error
5. left-before-right error location retained
6. optimized and unoptimized valid results agree

## Evidence

State-transition table, optimizer rules, equivalence tests, preserved-failure examples and restricted-termination argument.

## Transfer

A proposed rewrite replaces `x-x` with zero after the language adds effectful function calls. Explain which assumptions would be required before approving it.
