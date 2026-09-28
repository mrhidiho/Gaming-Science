# Demonstration result, not a completed learner Gate H

The reference case is a bounded fixed-point affine transform. It is a teaching example, not a production engine workload.

## Modeled alternatives

36 cases compare 1-, 2- and 4-lane alternatives at six sizes with normal and backpressured output. Every value was checked against the integer oracle. Timing assumes a 100 MHz clock; the clock and resource counts are NOT synthesis results.

The analytical end-to-end model includes 20 microseconds setup, 5 microseconds completion, 100 MB/s host payload transfer and 400 MB/s internal payload service. Units are decimal. Zero-size calls are skipped. These constants are educational assumptions, not hardware specifications.

| N | Lanes | Adverse | Modeled kernel us | Modeled end-to-end us |
|---|---|---|---|---|
| 1 | 1 | False | 0.040 | 25.080 |
| 1 | 1 | True | 0.040 | 25.080 |
| 1 | 2 | False | 0.040 | 25.080 |
| 1 | 2 | True | 0.040 | 25.080 |
| 1 | 4 | False | 0.040 | 25.080 |
| 1 | 4 | True | 0.040 | 25.080 |
| 64 | 1 | False | 0.670 | 28.230 |
| 64 | 1 | True | 1.310 | 28.870 |
| 64 | 2 | False | 0.640 | 28.200 |
| 64 | 2 | True | 0.670 | 28.230 |
| 64 | 4 | False | 0.640 | 28.200 |
| 64 | 4 | True | 0.640 | 28.200 |
| 65536 | 1 | False | 655.390 | 3301.830 |
| 65536 | 1 | True | 1310.750 | 3957.190 |
| 65536 | 2 | False | 655.360 | 3301.800 |
| 65536 | 2 | True | 655.390 | 3301.830 |
| 65536 | 4 | False | 655.360 | 3301.800 |
| 65536 | 4 | True | 655.360 | 3301.800 |

Four lanes do not automatically beat one. At the declared internal bandwidth, 4 bytes per item imposes 10 ns per item, already matching the one-lane asymptotic compute interval at 100 MHz. More lanes mainly shorten startup/drain effects or mitigate selected stalls; changing memory bandwidth can change that result.

## Host measurements

These are real timings of the provided C++ programs on the build host, not FPGA/GPU timings and not a measurement of the learner's machine. The contiguous loop is optimized by the compiler; the blocked loop is a second software candidate, not a promised improvement. No Python-to-hardware speedup claim is made.

| N | Variant | Median ns | p95 ns | Samples |
|---|---|---|---|---|
| 0 | contiguous | 30.0 | 31 | 30 |
| 0 | blocked | 30.0 | 31 | 30 |
| 1 | contiguous | 32.0 | 33 | 30 |
| 1 | blocked | 33.0 | 34 | 30 |
| 7 | contiguous | 46.0 | 50 | 30 |
| 7 | blocked | 53.0 | 54 | 30 |
| 64 | contiguous | 190.0 | 194 | 30 |
| 64 | blocked | 204.0 | 209 | 30 |
| 1024 | contiguous | 2629.5 | 4062 | 30 |
| 1024 | blocked | 2703.5 | 5869 | 30 |
| 65536 | contiguous | 166261.0 | 284377 | 30 |
| 65536 | blocked | 168627.5 | 236659 | 30 |

## What the learner still must do

Choose and measure an actual engine workload; set application-specific quality and latency tolerances; reproduce a competent baseline; adapt at least two architecture alternatives; sweep setup, transfer and internal bandwidth; retain small, large and adverse cases; and defend an independently reproduced conclusion. A software-only winning design is a valid outcome.

The supplied pipeline is an educational behavioral register model. It is not a tested board, synthesizable RTL, an ASIC estimate, an electrical design approval or evidence of console SDK access.
