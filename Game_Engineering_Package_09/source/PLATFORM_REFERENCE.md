# Platform and performance reference

## Units and boundaries
Use bytes for storage and explicitly distinguish decimal from binary prefixes. One MB is 1,000,000 bytes; one MiB is 1,048,576 bytes. GB/s is not Gb/s: eight bits make a byte before considering transport overhead. State whether bandwidth is raw signaling, effective payload or measured traffic at a particular memory level.

One millisecond is 1,000 microseconds; one microsecond is 1,000 nanoseconds. A timer returning nanoseconds does not necessarily have nanosecond resolution or accuracy. Watts are joules per second. Every reported latency, bandwidth and energy requires a boundary, clock or sensor scope and a useful-result definition.

## Formula sheet with assumptions
| Quantity | Formula | Required assumption |
|---|---|---|
| Wire time | bits / bit rate | Framing and overhead counted |
| Periodic utilization | sum(C_i/T_i) | Not alone a general deadline proof |
| Amdahl with overhead | 1 / [s + (1−s)/p + h] | Fixed useful work; h relative to original total time |
| Roofline | min(P_compute, B × intensity) | Same memory level and operation convention |
| Ridge intensity | P_compute / B | Consistent units and precision |
| Resource-service lower estimate | setup + max(demand/rate) | Ideal resource overlap; not guaranteed achieved |
| Serial comparison | setup + sum(demand/rate) | Selected serial schedule, not a universal upper bound |
| Transfer time | payload bytes / effective Bps | Rate and overlap explicitly stated |
| Energy, interval-average data | sum(P_i × delta_t_i) | P_i is interval average |
| Average power | energy / total time | Same measurement boundary |
| Useful efficiency | accepted work / joules | Quality held fixed; undefined at zero energy |
| Input-to-marker latency | t_marker − t_input | Calibrated/same clock; marker named accurately |
| Throughput FPS | 1000 / mean interval_ms | Completion intervals over elapsed time |
| Nearest-rank percentile | sorted[ceil(qN)−1] | 0<q<=1; finite sample, not a confidence guarantee |
| No-stall pipeline elapsed cycles | L + groups − 1 | Nonempty, II=1; first acceptance to last retirement |
| Maximum signed fixed-point value | (2^(bits−1)−1)/2^frac | Signed two's-complement raw range |
| Rigid inverse translation | −R^T p | R is an orthonormal rotation |

Zero-size operations need their own contract. The reference accelerator skips them and models zero setup; the native empty function is still timed to reveal harness/function overhead. Those two empty-case boundaries should not be presented as a measured accelerator speedup.

## The six-way separation
Addressability asks whether an address can be referenced. Placement asks where its backing storage resides. Coherence concerns visibility of updates within the supported system. Ordering concerns which operations may be observed before others. Ownership defines which participant may access a resource now. Completion identifies which operation has reached which boundary. None of these words is a universal synonym for another. [S05; S08; S09]

For any asynchronous request, record CPU writes, submission, device access, completion, CPU reads and reuse. A timeout ends a wait, not necessarily the device's access. Treat reset as safe only when its contract establishes quiescence. Stale-epoch checks are necessary logical protection in the teaching model but cannot stop real hardware writes.

## Interface checklist
Record electrical domains and pin direction; transport mode, framing and ordering; operation/format/length; units and timestamps; request identity and freshness; buffer size/stride/alignment; ownership; deadline and timeout origin; cancellation/reset; permissions/context; failure behavior and fallback. A named bus or API does not fill these fields automatically.

For optional physical work use exact part documentation, qualified review and a staged bring-up plan. Rule-check success is not proof of electrical safety. The curriculum does not provide a device-specific wiring or power-up authorization.

## Benchmark checklist
Define a relevant workload and equal useful quality. Keep oracle and performance baseline separate. Specify build options, timer boundaries, asynchronous completion, allocation, transfers and result consumption. Predeclare warmup/repetitions/order/exclusions. Reject wrong outputs and no-ops. Preserve all raw samples and metadata. Report sample count, central/tail measures and a reasoned uncertainty statement. Repeat a session and test small/tail/large/adverse inputs.

Use the whole application boundary for application claims. If only a kernel was timed, say so. A model-versus-measurement ratio remains conditional on the model. Do not convert a chosen clock, multiplier count or transfer rate into a product specification.

## Evidence tiers
| Tier | What it can establish | What it does not establish by itself |
|---|---|---|
| Analytical | Conditional bound or estimate from equations | Physical achieved timing |
| Functional model | Tested behavior under an abstraction | Clock closure, power or electrical behavior |
| Cycle model | Timing behavior under declared cycles/stalls | Accuracy of omitted hardware mechanisms |
| Synthesis | Target/tool-specific mapped structure and reports | A successfully measured board or full ASIC signoff |
| Host measurement | Executed host behavior at stated boundary | Modeled accelerator or another machine's performance |
| Physical measurement | Observed device behavior through a method | Universal conditions or unlimited correctness |

The package's real ledger checker verifies structure, relative paths and file hashes. Scientific sufficiency, fair baselines, correct units and valid inference remain review tasks. No automated “pass” should be described as peer-reviewed silicon validation.

## Numerical contract checklist
Specify signedness, width, fractional scale, intermediate precision, arithmetic order, rounding mode, saturation/wrap policy and exceptional values. Define allowed absolute/relative/application error and the distribution to which it applies. Test extremes, negative ties, threshold crossings and error accumulation. Report clipped results separately; a small mean error can hide a rare unacceptable output.

For the example Q8.8 format, one raw step is 1/256. Range is −128 to 127.99609375. Nearest-even ties map raw half-integers to the nearest even raw integer. The affine implementation rounds the scaled product before adding encoded bias; copying it into another arithmetic contract without that order is an implementation change.

## Latency and XR convention checklist
Name input generation and consumption events; simulation/render boundaries; software presentation marker; unknown optical stages; clock calibration; queue depth and percentile definition. Define spatial units, reference space, handedness, axis directions, pose sample time, prediction target time, validity and per-view projection source. Use rigid inverse transforms, not ad hoc position negation after arbitrary rotation. [S13; S16; S17]

The core traces are synthetic and the XR model is numerical. No optical latency, headset comfort or tracking accuracy was measured. A camera-transform test should not be described as a guarantee about users' physical experience.

## Glossary
**Arithmetic intensity:** Useful arithmetic operations divided by bytes transferred at a specified memory level.

**Backpressure:** A downstream consumer's inability to accept new work, propagated through a declared flow-control contract.

**Coalescing:** Combining related lane memory accesses into a more efficient set of transactions under a specific architecture.

**Critical path:** The dependency-constrained sequence that determines completion for the selected boundary.

**Deadline:** The latest allowed completion event for a particular job under a timing contract.

**Divergence:** Differing control-flow paths within a grouped execution mechanism that can require different masked work phases.

**Epoch/generation:** A lifetime identifier used to distinguish current resources or requests from stale ones.

**False sharing:** Coherence interference between distinct logical data items residing in the same coherence unit.

**Initiation interval:** The interval between successive accepted work groups in a pipeline, distinct from an individual group's latency.

**Occupancy:** A target-specific measure of resident execution resources; not itself a throughput guarantee.

**Oracle:** A trusted reference for expected behavior, ideally independently formulated for critical cases.

**Quiescence:** A state in which the relevant device activity has stopped sufficiently to permit the declared safe reuse or reconfiguration.

**SIMD / SIMT:** Different programming/execution abstractions for performing related operations across multiple lanes or logical threads; the selected architecture determines the detailed behavior.

**Saturation:** Clamping an out-of-range arithmetic result to the representable boundary instead of wrapping.

**Sensitivity analysis:** Examining how conclusions change as uncertain inputs, constraints or design parameters vary.

**Sustained performance:** Behavior over a stated longer workload window under the relevant operating policy, not merely an initial burst.
