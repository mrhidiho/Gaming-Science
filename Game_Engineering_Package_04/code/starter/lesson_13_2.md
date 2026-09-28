# Student contract 13.2: Stacks, queues and ring buffers

Implement a bounded queue with explicit full/empty results and wraparound tests. Pass: preserve FIFO order through more than three times its capacity in operations and never read an uninitialized slot.

1. Choose and document the count-based full/empty convention.
2. Implement bounded push/pop without dynamic allocation during operations.
3. Hand-trace wraparound at capacity three and test capacity one.
4. Differentially test a long deterministic operation sequence against std::deque and preserve the seed or trace.

## Cases

1. pop empty -> absent
2. push full -> false with unchanged state
3. capacity-one alternating operations
4. wraparound returns FIFO order
5. more than 3*capacity operations
6. no read from a logically empty slot

## Evidence

State-transition table, invariant checks, failure-policy documentation and differential-test trace.

## Transfer

An audio queue must never block but may drop old samples. Define a different overflow policy and identify which tests must change; do not silently reuse the command-queue contract.
