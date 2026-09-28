# Student contract 14.3: Dijkstra, A* and admissible heuristics

Implement Dijkstra and A* against the same grid model. Pass: compare path costs on many small maps, include no-path cases and demonstrate a deliberately overestimating heuristic that can sacrifice optimality.

1. Define neighbor rules, blocked cells, edge costs, distance bounds and tie-breaking.
2. Implement Dijkstra and A* with stale-entry handling and an explicit reopening policy.
3. Compare costs and independently validate routes over multiple small map families.
4. Demonstrate the overestimating-heuristic counterexample and record expansion/queue metrics without claiming universal speedup.

## Cases

1. start equals goal
2. unreachable region
3. weighted detour cheaper than direct route
4. zero-cost edge allowed
5. negative edge rejected
6. overestimating heuristic gives 10 versus optimal 2
7. A* with h=0 agrees with Dijkstra

## Evidence

Cost-model specification, path validator, small-map oracle, counterexample trace and comparative metrics.

## Transfer

Add diagonal movement with cost 1 while orthogonal movement also costs 1. Replace Manhattan with a valid lower bound and justify it.
