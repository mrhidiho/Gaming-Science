# Student contract 13.3: Hash tables and collision policies

Implement chaining or open addressing with collision tests and resizing. Pass: deliberately force many collisions, test missing keys and verify that distinct equal-hash keys remain distinct.

1. Implement a restricted chaining table with insert/update/find/erase and controlled resizing.
2. Check the full invariant after every mutation.
3. Force all keys to collide and test equal-hash distinct keys, updates and deletions.
4. Compare deterministic traces against std::unordered_map and report occupancy/probe observations separately from correctness.

## Cases

1. missing key -> absent
2. same key update does not increase size
3. distinct equal-hash keys preserved
4. erase chain head/middle/tail
5. all entries survive resize
6. negative and zero integer keys handled

## Evidence

Collision-policy specification, resize reasoning, invariant checks and differential mapping tests.

## Transfer

A mod supplies many deliberately colliding asset names. Explain why correctness tests are insufficient for a production resource-exhaustion defense.
