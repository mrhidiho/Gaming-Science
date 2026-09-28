# Reference evidence: keep the categories separate

## numerics/
These files are **numerical results from chosen mathematical models** and synthetic random trials. They are not physical motion measurements, collected player telemetry or hardware performance data. Regenerate them with capstone/reference/build_evidence.py into a new output directory.

The trajectory tables compare integrators against analytic motion at a shared final time. The derivative and quadrature tables include numerical error. The sampling/filter files expose known alias and boundary behavior. Seeded categorical counts illustrate sampling variation. Reusing a seed across sample counts can share prefixes, so those counts are not independent replications across sizes. Optimization tables preserve iteration-limit and adverse cases. metadata.json records assumptions and environment.

## measured_benchmark/
These are **actual elapsed-time observations** taken in the authoring environment, not invented timings. raw_trials.csv contains 360 observations: six workload configurations, 30 paired trials and two algorithms. summary.csv summarizes those observations. metadata.json records the Python/platform version, included/excluded costs, seed, ordering and inference limitations.

Method A performs membership queries on a list. Method B builds a set and performs the same queries, with set-building cost included. Neither result predicts native engine, GPU or another computer's performance. Consecutive trials on shared infrastructure may not satisfy the independent normal paired-difference model behind the conditional t intervals. Rerunning the benchmark produces new timings and should not reproduce these numbers byte-for-byte.

## data/ elsewhere in the package
The two CSVs under the package's top-level data/ folder are explicitly **synthetic teaching data**, not benchmark observations. Do not merge those values into the actual measured trial table.

Use capstone/reference/REFERENCE_NOTEBOOK.md to connect this evidence to a small written argument. It is supplied reference work, not an independently completed student submission or defense.
