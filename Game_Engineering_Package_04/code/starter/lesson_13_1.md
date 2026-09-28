# Student contract 13.1: Complexity, arrays and linked structures

Implement a growable integer buffer for study. Count copied elements under doubling and one-at-a-time growth. Pass: derive the growth behavior and separately measure elapsed time without equating it to the proof.

1. Implement an integer-only buffer with size/capacity invariants and two growth policies.
2. Instrument relocated-element counts and predict the sequence for n = 8 and n = 9.
3. Test value preservation, empty access, exact growth boundaries and a chosen capacity budget.
4. Compare counts analytically, then collect separate Release timings against std::vector.

## Cases

1. empty buffer has size 0
2. out-of-range access rejected
3. n=8 exact-fit moves 28; doubling moves 7
4. n=9 doubling moves 15
5. values preserved through growth
6. capacity limit checked before arithmetic

## Evidence

Growth trace, geometric-series argument, invariant tests and timing results separated from the proof.

## Transfer

A game must never allocate during a frame. Explain why amortized O(1) is insufficient and design a capacity-planning policy with an explicit failure result.
