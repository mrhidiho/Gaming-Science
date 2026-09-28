# Student contract 14.4: Dynamic programming, complexity limits and approximation

Solve a small 0/1 knapsack instance by exhaustive search and dynamic programming. Pass: compare answers, derive state count, and describe how a heuristic would be evaluated without claiming a guarantee it lacks.

1. Define item and capacity domains and derive the include/exclude recurrence.
2. Implement exhaustive search with a small explicit item-count cap.
3. Implement dynamic programming, checking capacity allocation and value arithmetic.
4. Differentially test small instances and compare one heuristic without overstating its guarantee.

## Cases

1. no items -> 0
2. capacity zero -> 0
3. all items too heavy -> 0
4. (2,3),(3,4),(4,5), B=5 -> 7
5. single (2,3), B=4 -> 3, not 6
6. many deterministic small cases agree with exhaustive solver

## Evidence

State definition, recurrence proof, loop-order explanation, oracle comparisons and quality evaluation of a heuristic.

## Transfer

The loadout now limits both mass and electrical power. Define the new sufficient state and explain the growth in table size before implementing it.
