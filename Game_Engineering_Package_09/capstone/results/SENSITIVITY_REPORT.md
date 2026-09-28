# Sensitivity of the teaching model

972 analytical combinations reuse the 36 validated functional traces. Setup, host payload bandwidth and internal payload bandwidth each take three declared values. These are hypothetical assumptions, not measured device properties.

The table holds setup at 20 us, completion at 5 us and selects N=65,536, four lanes, normal readiness. Only the two bandwidth assumptions change.

| Host MB/s | Internal MB/s | Conditional end-to-end us |
|---|---|---|
| 25 | 100 | 13132.200 |
| 25 | 400 | 11166.120 |
| 25 | 1600 | 10674.630 |
| 100 | 100 | 5267.880 |
| 100 | 400 | 3301.800 |
| 100 | 1600 | 2810.310 |
| 400 | 100 | 3301.800 |
| 400 | 400 | 1335.720 |
| 400 | 1600 | 844.230 |

Higher internal bandwidth alone does not remove host transfers. At each bandwidth pair, setup values 5 and 80 us shift a nonempty result by −15 and +60 us relative to this table. An engine decision still needs measured workload frequency and an application critical-path model.

Reproduce in a new folder with: `python -m capstone.sensitivity --input my_results/model_only/model_results.json --output my_results/model_only`. Changing compute architecture or clock requires a corresponding justified model, not only editing these costs.
