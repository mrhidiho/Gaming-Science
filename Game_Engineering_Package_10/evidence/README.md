# Evidence boundaries

`reference_run` is a recorded diagnostic run of the supplied educational references, not a completed learner submission or an independent reproduction of a research paper. All input workloads here are small synthetic examples. Preserve this directory and write your own runs elsewhere.

| File family | What it supports | What it does not establish |
|---|---|---|
| numerical.csv | Known-solution solver behavior on four diagonal conditioning levels | General sparse performance, full SPD verification or preconditioner superiority |
| scan_cases.csv | Exact CPU scan checks at selected boundary sizes | GPU correctness or acceleration |
| pipeline_model.json / schedule_model.json | Consequences of declared analytical timing/scheduling assumptions | Physical overlap, device occupancy or real queue throughput |
| bar_sensitivity.csv | One-dimensional linear-chain error against a same-discretization dense oracle; one CPU duration per case | Three-dimensional cloth validity, full XPBD paper reproduction, stable performance estimates |
| render_*_linear.json / .ppm | Executed small grayscale path tracer; linear values and tone-mapped previews | Equal-quality speedup or a converged ground-truth image |
| mis_integral_trials.csv | Seeded repeated estimates of a known one-dimensional integral | Rendering-scene generalization or a full reservoir-reuse estimator |
| stream_trace.json / lifecycle.json | Bounded resource model behavior and an intentional safety counterexample | Real I/O completion guarantees, distributed durability or proven liveness |
| compiler_semantics.json / generated_kernel.cpp | Restricted u32 expression agreement and generated source | A full optimizer, dominance verifier, native JIT or security sandbox |
| native_scan_pairs.csv | Within-process CPU benchmark observations for one workload | Independent run/scene uncertainty or cross-machine performance |
| run_environment.json | Recorded interpreter/platform, command and reference-source hashes | Reproducibility on untested devices |

Use `validation` for actual package test logs. A passing log verifies only its stated checks. A reviewer must independently rerun the learner's central Gate I result before that gate is marked complete. Preview PPM values are tone-mapped; use linear JSON values for numerical image comparisons. Never relabel model times as measurements.
