# Student contract 14.2: Graph traversal and dependency ordering

Implement BFS and topological sorting. Pass: recover a shortest unweighted path, report unreachable goals, reject a cyclic dependency graph and justify the O(V+E) traversal bound for adjacency lists.

1. Specify graph direction, vertex domain and duplicate-edge policy.
2. Implement BFS with predecessor reconstruction and explicit unreachable results.
3. Implement Kahn topological sorting and reject cyclic inputs.
4. Validate path edges and every dependency relation, then justify the bound for your chosen frontier and representation.

## Cases

1. source equals goal
2. isolated unreachable goal
3. diamond graph with two shortest paths
4. directed cycle
5. self-loop cycle
6. disconnected DAG includes all vertices
7. invalid vertex rejected

## Evidence

Annotated graphs, predecessor traces, order validator, cycle tests and representation-specific complexity argument.

## Transfer

A planner uses a priority queue to choose the alphabetically smallest ready asset. Update its complexity analysis instead of retaining an unqualified O(V+E) claim.
