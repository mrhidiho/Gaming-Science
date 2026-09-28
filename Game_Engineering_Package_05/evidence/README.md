# Evidence index

These files are observations from package-development validation, not results produced by the learner. See ../VALIDATION.md for the final test counts and exact environment.

`environment.json` records actual tools. `DEMO_OUTPUTS.json` records the twenty example outputs. The same deterministic strings are in `data/expected_examples.json` for fresh-run checks; comparison ignores leading/trailing whitespace, not substantive content.

The four CSV files are actual timings from this container. All time units are defined in their headers. There is no universal speedup target. Randomized order, correctness checks and workload construction are defined by the corresponding native source files. These are short, shared-container measurements—not hardware specifications or a steady-state device certification.

`arithmetic_benchmark.csv` compares serial/four-accumulator kernels across three sizes. Both may be vectorized by the compiler. `locality_benchmark.csv` uses full permutations that visit the same elements; its timed indirect accesses include the index-array traffic. `false_sharing.csv` compares a compact layout with a chosen 64-byte-aligned layout; 64 is not a measured cache-line claim, and thread startup is included. `graph_scaling.csv` includes task scheduling and worker startup for 1, 2 and 4 workers.

`vectorization_gcc.txt` and `kernels_host.s` are actual host compiler output for the specific source and options in the systems reference. RISC-V assembly was assembled separately, not executed. `sqlite_query_plan.json` is an actual before/after query-plan observation on an explicitly generated fixture, not player telemetry. Validation logs retain exact commands and results; paths identify the build environment.
