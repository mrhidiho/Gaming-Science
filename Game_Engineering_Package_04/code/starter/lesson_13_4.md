# Student contract 13.4: Trees, heaps and priority queues

Implement a binary min-heap with push/pop and randomized comparison to a sorted reference. Pass: validate the heap invariant after every operation and test duplicate priorities.

1. Implement a binary min-heap with explicit empty behavior and a size budget.
2. Validate parent/child order after every mutation.
3. Compare push/pop traces with a sorted independent oracle, including duplicates.
4. Add an event-priority tie-breaker and compare heap requirements with balanced-tree requirements.

## Cases

1. empty pop -> absent
2. one-element pop leaves empty
3. ascending and descending insertions
4. duplicate priorities retained
5. negative priorities ordered correctly
6. invariant after every randomized operation

## Evidence

Index diagram, sift traces, invariant checker, differential tests and a data-structure decision table.

## Transfer

A scheduler now needs all events whose times lie in an interval, not only the next event. Reconsider the structure and explain the changed query cost.
