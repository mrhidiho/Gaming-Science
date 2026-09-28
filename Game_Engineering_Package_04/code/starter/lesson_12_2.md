# Student contract 12.2: Copy, move and exception safety

Implement a move-only mock resource and transactional asset replacement. Pass: copying is prohibited, moving does not double-release, and injected load failure preserves the old asset.

1. Implement a move-only mock owner or explain a rule-of-zero alternative.
2. Add compile-time tests proving copying is prohibited and move construction is supported.
3. Build a transactional replacement function and inject failures before commit.
4. Measure the maximum simultaneous live-resource count and state the memory tradeoff.

## Cases

1. copy constructible is false
2. move leaves exactly one owning handle
3. move assignment releases prior destination
4. self-move remains valid
5. load/validation failure preserves old asset
6. successful replacement releases old asset once

## Evidence

Ownership transfer trace, compile-time constraints, failure matrix and a statement of basic/strong/no-throw guarantees.

## Transfer

A reload operation updates both an asset and an ID index. Show why swapping only the asset may not provide the strong guarantee for the whole repository.
