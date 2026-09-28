# Student contract 14.1: Searching, sorting and algorithm selection

Implement binary search with a documented interval convention and test empty, one-element, duplicate and missing cases. Compare two sorts on random and nearly sorted inputs. Pass: verify output order and element preservation.

1. Implement lower bound with a written half-open invariant and a separate membership wrapper.
2. Test empty, singleton, duplicate and missing targets against the standard lower-bound algorithm.
3. Implement or inspect insertion and merge sorts, checking order, multiset preservation and stability as applicable.
4. Compare random and nearly sorted inputs with saved data and repeatable Release measurements.

## Cases

1. empty -> insertion position 0
2. target below all -> 0
3. duplicate target -> first equivalent position
4. target above all -> size
5. sorting preserves duplicate counts
6. equal-key records preserve order for stable implementation

## Evidence

Binary-search proof sketch, boundary tests, sorting property tests and distribution-specific comparison.

## Transfer

The comparator sorts asset names case-insensitively, but search uses case-sensitive comparison. Explain why the search precondition is broken.
