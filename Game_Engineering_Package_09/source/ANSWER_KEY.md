# Answer key and review guidance

## Use after an independent attempt
This key contains answers for 100 lesson questions, 40 written problems, 25 module-review questions and ten diagnostic questions. The original first three lesson questions are marked original; the fourth and fifth are expansion questions. Questions and answers are repeated together for unambiguous self-checking.

Use the answer to repair the reasoning, not just memorize the wording. An answer that omits a required boundary—such as modeled rather than measured, or timeout rather than quiescence—may remain incorrect even if its numerical value matches. Reference code under labs/reference demonstrates the computational slices. Full practical work and capstone architecture choices require the evidence and rubrics in the workbook and capstone specification rather than one universal solution file.

## Diagnostic answers

### D01
**Question:** A 32-bit word starts at address 62 and a modeled sector is 64 bytes. How many sectors can it touch?

**Answer:** Two: bytes 62–65 cross the boundary at 64. Distinguish word size from alignment.

### D02
**Question:** Does a volatile C++ pointer establish CPU/device ownership or API-specific synchronization?

**Answer:** No. A language qualifier does not substitute for the platform’s synchronization and mapping contract.

### D03
**Question:** A 10 ms frame contains a 2 ms serial operation. What is the maximum additive-frame speedup if it disappears?

**Answer:** 10/8 = 1.25x. The maximum time reduction is 20%, assuming the operation is on the critical path.

### D04
**Question:** Explain why deadline and average utilization are different concepts.

**Answer:** A deadline constrains a particular job’s completion. Utilization summarizes demand over time and does not by itself prove every job meets a deadline under all scheduling and blocking assumptions.

### D05
**Question:** What is the difference between a functional model and a physically measured circuit?

**Answer:** The model executes a stated abstraction. A physical measurement observes a built circuit through an instrument and method. Each has limits; functional correctness does not establish physical timing or power.

### D06
**Question:** A camera pose has rotation R and position p. Give the rigid world-to-camera inverse.

**Answer:** Rotation R transpose and translation −R transpose times p, assuming R is an orthonormal rotation.

### D07
**Question:** What evidence should accompany a claimed faster algorithm?

**Answer:** Correct outputs at the same quality, an appropriate baseline, raw timings, workload and environment metadata, boundaries, repeat policy and a defensible uncertainty statement.

### D08
**Question:** Why can a timeout fail to make a device buffer safe to reuse?

**Answer:** The device may still access it. Completion or acknowledged quiescence is needed under the ownership contract.

### D09
**Question:** Convert 3 MiB and 3 MB to bytes.

**Answer:** 3 MiB = 3×1,048,576 = 3,145,728 bytes. 3 MB = 3,000,000 bytes in decimal units.

### D10
**Question:** What must happen before optional physical board bring-up?

**Answer:** Use the exact board/peripheral documentation and obtain qualified review of electrical limits, power, wiring, layout and bring-up plan. Simulation and rule-check success are not electrical approval.


## Module 36 — Answers


### Lesson 36.1 — Serial interfaces and peripheral contracts

**Q1 (original). Why can two SPI devices fail at the same clock rate?**

Clock rate does not specify polarity, phase, bit order, selection timing or the peripheral command protocol. Matching frequency while sampling on the wrong edge can corrupt data; compare the complete endpoint contracts.

**Q2 (original). Does an interface name guarantee voltage compatibility?**

No. The physical devices must agree on supported voltage ranges, thresholds, pin directions and loading. A familiar interface label does not make a connection electrically compatible.

**Q3 (original). Why begin with one interface rather than every bus?**

One interface bounds the state space and makes failures attributable. First establish known-good transactions, fault detection and recovery; then extend the driver without losing those tests.

**Q4 (expansion). A five-byte transfer uses a 1 MHz clock plus 10 microseconds of mandatory overhead. Can a 40-microsecond total deadline succeed?**

No under this serial timing model. The wire consumes 40 microseconds and mandatory overhead adds 10, so the minimum is 50 microseconds before software delay.

**Q5 (expansion). Does a valid XOR check prove that the device used the correct SPI mode or that the sender is authentic?**

Neither. Different errors can preserve XOR, and XOR contains no secret or authenticity guarantee. Simulator mode metadata is stronger information than real decoded bytes alone.

**Written problems — worked guidance**

**P36.1-A. For UART 8-N-1 at 115200 bit/s, derive the minimum wire time for a 12-byte payload, ignoring interbyte gaps.**

Each byte consumes one start, eight data and one stop bit: 10 bits. Total time is 120/115200 s = 1.041667 ms. This excludes device processing and scheduling.

**P36.1-B. A device allows at most 100 microseconds from request start to valid reply. Wire time is 50, processing is bounded at 20, and host jitter is bounded at 18 microseconds. What margin remains?**

The budget consumes 50 + 20 + 18 = 88 microseconds, leaving 12 microseconds. This is meaningful only if each component is a valid bound and the phases are nonoverlapping.

**Published example output**

```json
{
  "status": "ok",
  "value": 5
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 36.2 — Firmware, RTOS scheduling and driver lifecycle

**Q1 (original). Does an RTOS automatically make all tasks meet deadlines?**

No. Deadline satisfaction depends on bounded execution, arrivals, blocking, interrupt load, priorities and resource contention. The RTOS provides mechanisms; the application supplies a schedulable design.

**Q2 (original). Why not feed a watchdog unconditionally from a stuck loop?**

It can conceal lack of forward progress. Supervision should depend on critical work advancing, not merely on some loop or interrupt remaining alive.

**Q3 (original). What must happen to outstanding requests when a device disappears?**

Prevent new submissions, cancel or complete pending requests according to the contract, establish quiescence before freeing device-owned storage, and reject stale callbacks. Each request receives a single terminal outcome.

**Q4 (expansion). A task is released at tick 0 with a deadline at tick 4 and completes on edge 4. Is it late in the supplied model?**

No. Completion at the deadline is accepted. Finishing on edge 5 would be late; the model counts a miss at edge 4 while it is unfinished.

**Q5 (expansion). Why does a reset generation counter not by itself make old DMA buffers safe to free?**

It filters stale software completions, but cannot prevent a device from physically writing memory. The reset/cancellation mechanism must also establish that old accesses have stopped.

**Written problems — worked guidance**

**P36.2-A. Compute utilization for C/T values 1/5, 2/10 and 3/20. Does the sum establish deadlines?**

U = 0.2 + 0.2 + 0.15 = 0.55. The unused average capacity is 45%, but this alone does not bound priority-dependent response time, blocking or jitter.

**P36.2-B. A deadline is 5 ms. The task needs 1 ms of execution, waits 3 ms on a lock, and suffers 2 ms of higher-priority interference. Can that response meet the deadline under an additive model?**

No. The response requires 1 + 3 + 2 = 6 ms, missing the 5 ms deadline by 1 ms. Lower average CPU utilization elsewhere does not fix this dependency.

**Published example output**

```json
{
  "released": 2,
  "completed": 2,
  "missed": 0,
  "pending": 0
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 36.3 — Schematics, PCB layout, power integrity and signal integrity

**Q1 (original). Does passing DRC prove electrical correctness?**

No. DRC evaluates configured geometric and connectivity rules. A wrong footprint, inappropriate part, unreviewed voltage domain or flawed power strategy can remain despite a clean report.

**Q2 (original). Why do return paths matter?**

The outgoing signal and returning current form a physical loop. The return geometry affects impedance, coupling and noise; a discontinuity can damage signal quality even when schematic connectivity is correct.

**Q3 (original). Why verify footprints against datasheets?**

Symbols and library footprints may differ from the actual package or orientation. Check pad numbers, pitch, dimensions, pin-1 marking and connector mating view against the exact component documentation.

**Q4 (expansion). A 65 mA steady load fits a 100 mA budget. What information is still needed before approving the supply?**

Startup and transient demand, component tolerances, regulator behavior, voltage drop, operating conditions and allowable rail variation. A steady-state sum does not establish transient integrity.

**Q5 (expansion). Is the supplied board-review JSON checker sufficient to complete the original KiCad assignment?**

No. It checks only a few declared fields. The learner must create and review the schematic/layout, verify exact footprints and preserve ERC/DRC evidence.

**Written problems — worked guidance**

**P36.3-A. An ideal 25 mA transient lasts 4 microseconds. What capacitance limits ideal droop to 50 mV?**

C = 0.025 A * 4e-6 s / 0.05 V = 2e-6 F = 2 microfarads. Real parasitics and regulator behavior still require analysis.

**P36.3-B. A connector drawing labels pin 1 on the left when viewed from the mating side. A footprint screenshot labels pin 1 on the right from the component side. Is one necessarily wrong?**

No. The views can be mirrored by their different viewing directions. Establish the exact orientation, board side and mating geometry before comparing positions; verify numbered contacts, not visual left/right alone.

**Published example output**

```json
{
  "issues": [],
  "ready_for_review": true
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 36.4 — Bring-up, instrumentation and fault isolation

**Q1 (original). Why test power, clock and reset before complex application behavior?**

Power, clock and reset are prerequisites for meaningful application behavior. A downstream command failure cannot identify a software defect while one of those dependencies is absent.

**Q2 (original). What is the value of an expected-observation table?**

It connects a hypothesis to a discriminating observation and an explicit next branch. It makes the procedure repeatable and exposes missing or unsafe assumptions.

**Q3 (original). What should happen when a physical observation exceeds a reviewed safe limit?**

Stop the physical activity according to the reviewed procedure, isolate the setup safely, preserve evidence and request qualified review. Do not continue debugging by bypassing the limit.

**Q4 (expansion). The identity register fails while the modeled clock is missing. Which branch should the procedure inspect first, and why?**

The clock branch. The missing prerequisite can explain the downstream identity failure; diagnosing the register first would confuse a symptom with an independent cause.

**Q5 (expansion). Why must a trace identify the firmware build and decoder configuration?**

Otherwise the same bytes or waveforms may be interpreted under the wrong protocol or compared against different code. Provenance is needed to reproduce and interpret the observation.

**Written problems — worked guidance**

**P36.4-A. Two hypotheses are wrong bus mode and missing clock. The decoder reports zeros for every reply. What extra observation discriminates better than repeating the read?**

Observe whether clock transitions exist under the declared selection window. An absent clock supports the clock hypothesis; recorded edges permit subsequent mode/timing analysis. All-zero decoded bytes alone are ambiguous.

**P36.4-B. A simulated setup exceeds its declared current budget and also reports an incorrect device ID. Which result has priority?**

The over-limit stop condition. Functional diagnosis resumes only after the safety condition is resolved under review; the incorrect ID does not justify continued operation.

**Published example output**

```json
{
  "action": "RUN_BOUNDED_SELF_TEST"
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Module 36 — Review answers

**R36-1. A controller returns a checksum-valid packet with an old sequence after a retry. Explain what additional contract is needed.**

A checksum does not prove freshness. Define request identity, acceptable sequence progression, wraparound/reset behavior and a bounded stale-response policy. Do not silently accept the old input as a current observation.

**R36-2. An input task misses its deadline while average CPU load is 40%. Give a plausible structural cause and an experiment.**

Blocking on low-priority logging, a long nonpreemptible interval or interrupt interference can dominate response. Trace releases, blocking and completion, then remove or bound the suspected critical-path dependency while holding other work constant.

**R36-3. A board passes DRC but a connector footprint was mirrored. Explain why DRC may not catch the error.**

DRC checks declared geometrical/electrical rules, not whether the designer chose the correct physical connector view and pin mapping. Compare footprint numbering and orientation with the exact datasheet and schematic intent.

**R36-4. Power is within the reviewed limit, reset is released, clock is absent and identity reads fail. Which hypothesis should be tested first?**

The missing clock is an earlier prerequisite. Confirm the observation and its expected source before debugging high-level identity logic. If any observation exceeds a reviewed safe limit, stop and isolate instead.

**R36-5. Define evidence sufficient for the simulated peripheral project and evidence still needed for fabrication.**

Simulation evidence includes framing/error tests, bounded scheduling and ownership traces, interface specification, schematic/layout files and review findings. Fabrication additionally needs qualified electrical/layout/footprint/power/bring-up review using exact parts; simulation alone cannot authorize it.


## Module 37 — Answers


### Lesson 37.1 — SIMT execution, divergence, occupancy and latency hiding

**Q1 (original). What is branch divergence in grouped GPU execution?**

Divergence occurs when lanes in an execution group follow different control-flow paths. The group may issue multiple paths with only subsets of lanes active, depending on the architecture and compiled code.

**Q2 (original). Does high occupancy guarantee high throughput?**

No. Occupancy is a residency measure. Throughput can still be limited by dependencies, memory service, instruction mix, execution resources or insufficient useful work.

**Q3 (original). Why can reducing register use sometimes hurt?**

It can introduce register spills, additional memory traffic or recomputation, or reduce instruction-level parallelism. A residency gain must be evaluated against those costs.

**Q4 (expansion). In a four-lane group with two lanes on each of two four-slot paths and no common prefix, what is useful lane-slot efficiency?**

The group issues 8 slots across 4 lanes, giving 32 opportunities. Useful work is 4 lanes * 4 slots = 16, so efficiency is 16/32 = 50%.

**Q5 (expansion). A new kernel lowers occupancy from 100% to 50% but runs faster. Is the measurement inherently invalid?**

No. More registers per thread may reduce spills or preserve reuse. Validate outputs and timing boundaries, then use counters or controlled changes to investigate why it improved.

**Written problems — worked guidance**

**P37.1-A. A hypothetical register file has 32768 registers. Each 128-thread block uses 64 registers per thread. Ignoring every other limit, how many blocks fit?**

Each block uses 128*64=8192 registers. floor(32768/8192)=4 blocks fit. This is only the register-capacity constraint.

**P37.1-B. Three of four lanes use a one-slot path; one uses a nine-slot path. With no common prefix, compute useful lane-slot efficiency.**

Both paths are issued, totaling 10 slots across 4 lanes = 40 opportunities. Useful work is 3*1+1*9=12, so efficiency is 30%.

**Published example output**

```json
{
  "issued_slots": 4,
  "useful_lane_slots": 16,
  "efficiency": 1.0
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 37.2 — Coalescing, local storage, caches and shared-memory banks

**Q1 (original). What does coalescing improve?**

It can reduce the number of memory transactions required to service a grouped instruction, increasing useful bytes per serviced transaction under the selected memory rules.

**Q2 (original). Why can shared memory still cause stalls?**

Shared storage can encounter bank conflicts, dependencies, synchronization waits and capacity-related occupancy limits. Being on chip does not make every access free or conflict-free.

**Q3 (original). Why include layout conversion in a comparison?**

Conversion is work caused by the optimization. Excluding it can make a slower application look faster; amortization is justified only when the converted representation is actually reused.

**Q4 (expansion). Why does a four-byte access at byte address 30 touch two 32-byte sectors?**

It spans bytes 30,31,32,33. The first two bytes are in sector 0 and the last two in sector 1.

**Q5 (expansion). When can a 0.7 ms conversion followed by a 0.6 ms kernel beat an original 1.0 ms kernel?**

For k reusable invocations, require 0.7+0.6k < 1.0k, so k > 1.75. Two or more invocations win under these assumptions, provided no extra reconversion or ordering cost is omitted.

**Written problems — worked guidance**

**P37.2-A. Eight four-byte words start at addresses 4,8,...,32 with 32-byte sectors. How many sectors and useful bytes are involved?**

The words span bytes 4 through 35, touching sectors 0 and 1. There are 32 unique useful bytes and 64 modeled transferred bytes, so utilization is 50%.

**P37.2-B. A read group requests word addresses 0,32,64,96 in a 32-bank model. Compare with addresses 0,0,0,0.**

The first group requests four distinct words in bank 0, giving a modeled four-way conflict. The second requests one word repeatedly and is a broadcast read, modeled as one bank service.

**Published example output**

```json
{
  "sectors": 4,
  "transferred_bytes": 128,
  "useful_unique_bytes": 128,
  "utilization": 1.0
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 37.3 — Raster, texture, matrix and ray-tracing units

**Q1 (original). Does a ray-tracing unit eliminate the rest of rendering work?**

No. It accelerates selected ray-related operations; other rendering work, data-structure preparation, shading and memory movement still contribute to the frame.

**Q2 (original). Why compare the same numerical precision or quality?**

Otherwise the candidates may solve different problems. State the error or quality target and verify both candidates satisfy it before comparing speed or energy.

**Q3 (original). When might specialized hardware lose on a small workload?**

Launch, setup, transfer, conversion and synchronization can dominate the small amount of useful arithmetic. The per-item advantage may appear only beyond a crossover size.

**Q4 (expansion). A path costs 20 microseconds setup plus 0.05 microseconds per item; the baseline costs 0.2 microseconds per item. At what first integer size does it win?**

20+0.05N < 0.2N implies N>133.333..., so the first winning integer is 134, excluding all other overhead.

**Q5 (expansion). Why is the sum of independent resource-service estimates not a guaranteed upper bound on observed latency?**

Unmodeled dependencies, contention, queuing, launch overhead and memory behavior may add delay. It is a serial-service comparator under stated assumptions, not a universal latency bound.

**Written problems — worked guidance**

**P37.3-A. Arithmetic service is 3 ms, ray service is 5 ms and setup is 0.4 ms. Give the ideal-overlap lower estimate and serial-service comparator.**

Ideal overlap is 0.4+max(3,5)=5.4 ms. Serial service is 0.4+3+5=8.4 ms. Additional unmodeled costs can exceed either estimate.

**P37.3-B. A specialized path has lower mean image error but creates one severe outlier in 1000 frames. What should the comparison report?**

Report both aggregate and tail/maximum quality behavior, retain the failing frame and compare against the declared acceptance criterion. Lower mean error cannot waive an explicitly unacceptable artifact.

**Published example output**

```json
{
  "lower_s": 1.1,
  "serial_s": 1.3,
  "dominant": "alu"
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 37.4 — CPU-GPU sharing, discrete memory and synchronization

**Q1 (original). Does shared addressing mean zero data-access cost?**

No. Memory access still consumes service time and bandwidth; shared resources can incur coherence, synchronization, migration or contention costs depending on the platform.

**Q2 (original). Why is CPU modification during GPU use risky?**

The CPU can race with device reads or writes, producing inconsistent input or overwritten output. Observe the API-specific ownership and synchronization contract before modifying or reusing storage.

**Q3 (original). What must an end-to-end accelerator benchmark include?**

Input preparation, setup, transfers or visibility work, dispatch, kernel execution, synchronization, result consumption and any required fallback. Report which phases are included and which resources overlap.

**Q4 (expansion). Why can a timed-out request still own its buffer?**

The device may continue to access it after the host stops waiting. Quarantine or retain ownership until completion or confirmed quiescence makes reuse safe.

**Q5 (expansion). Does double buffering automatically halve single-request latency?**

No. It can overlap different requests and improve the completion interval. Each request still experiences its required stages, and added queueing may increase latency.

**Written problems — worked guidance**

**P37.4-A. Upload is 0.3 ms, compute 0.8 ms and readback 0.2 ms. Ignoring all other work, compare serialized one-request latency with the ideal steady interval of three independent stages.**

Serialized latency is 1.3 ms. Ideal steady interval is max(0.3,0.8,0.2)=0.8 ms when requests overlap and resources are truly independent. This does not imply 0.8 ms single-request latency.

**P37.4-B. A buffer has been submitted but the host wait times out. Name two conditions that could safely enable eventual reuse.**

A valid completion accepted under the ownership policy, or a reset/cancellation sequence that confirms the device is quiescent and can no longer access that buffer. A timeout alone is insufficient.

**Published example output**

```json
{
  "transfer_or_visibility_s": 2.0,
  "latency_s": 2.4
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Module 37 — Review answers

**R37-1. A shader changes from 100% to 75% theoretical occupancy and becomes faster. Is this contradictory?**

No. Occupancy is one resource-related measure. Lower occupancy can accompany less spilling, greater instruction-level parallelism or lower synchronization cost. Measure the actual kernel and inspect the changed bottleneck.

**R37-2. A layout reduces modeled sectors by half but adds a conversion pass. State the correct comparison.**

Compare the full consuming pipeline at equal output quality, including conversion, allocation, transfers and reuse frequency. The sector count is a mechanism estimate, not an end-to-end result.

**R37-3. A matrix unit has high nominal arithmetic throughput. Why might a small transform batch lose?**

Setup, packing, supported precision, shape mismatch, data movement, dispatch and underutilization can dominate. A competent direct CPU/GPU path may be better at that size.

**R37-4. Shared addressing is available. Which other questions remain before CPU/GPU overlap is correct?**

Where data resides, how visibility and ordering are established, who owns each buffer, when completion permits reuse, and what happens under migration, failure or timeout. Shared addresses do not answer these questions.

**R37-5. Explain how to use a GPU-less architecture workbook honestly.**

Label group/sector/bank/resource numbers as model assumptions, verify them analytically, and avoid claims about a named GPU’s measured behavior. Identify the profiler and target evidence needed to test each hardware hypothesis later.


## Module 38 — Answers


### Lesson 38.1 — Amdahl, roofline and bottleneck models

**Q1 (original). What is the example roofline bound?**

The original example is min(1,000 GFLOP/s, 100 GB/s × 2 FLOP/byte) = 200 GFLOP/s. It uses decimal units and an explicitly declared memory level.

**Q2 (original). What is the maximum speedup with 20% unchanged serial work and infinitely fast remaining work?**

Five times: the remaining time approaches 0.2 of the original, so speedup approaches 1/0.2 = 5 when no new overhead is added.

**Q3 (original). Does being below the roof prove the model is wrong?**

No. A ceiling need not be reached. Dependencies, small workloads, synchronization, other resources or incomplete assumptions can keep execution below it.

**Q4 (expansion). A kernel is 10% of a frame and becomes twice as fast without overhead. What is frame speedup?**

New normalized time is 0.9 + 0.1/2 = 0.95; speedup is 1/0.95 ≈ 1.0526. Frame time falls by 5%, not 50%.

**Q5 (expansion). Why must intensity and bandwidth refer to the same memory level?**

The byte count must describe the traffic served by the resource whose rate is used. Pairing DRAM traffic with cache bandwidth creates a physically inconsistent ceiling.

**Written problems — worked guidance**

**P38.1-A. A frame has unchanged fraction 0.3; the remainder improves 5x and new overhead is 0.06 of original time. Find speedup.**

New time fraction = 0.3 + 0.7/5 + 0.06 = 0.50. Speedup = 2.0. With no overhead it would be 1/0.44 ≈ 2.2727.

**P38.1-B. Compute ceiling is 600 GFLOP/s and DRAM bandwidth is 75 GB/s. At 4 FLOP/byte, find the roof and ridge.**

Bandwidth ceiling = 300 GFLOP/s, so the roof is 300 GFLOP/s. Ridge intensity = 600/75 = 8 FLOP/byte.

**Published example output**

```json
{
  "speedup": 2.5,
  "roof_GFLOPs": 200
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 38.2 — Profilers, counters and trustworthy benchmark design

**Q1 (original). Why validate benchmark output?**

Otherwise a no-op, dropped tail, stale buffer or unacceptable approximation can appear to be an optimization. Validate the same useful result before accepting a performance claim.

**Q2 (original). Are similarly named counters identical across all processors?**

No. Event definitions, scopes, collection behavior and supported counters differ. Use the selected architecture and tool documentation.

**Q3 (original). Why declare an exclusion policy before inspecting results?**

To prevent removing inconvenient observations after seeing them. A declared policy supports an auditable comparison; raw samples and reasons must remain available.

**Q4 (expansion). For five samples 10,10,11,12,40 ms, what are median and nearest-rank p95?**

Median is 11 ms. p95 uses rank ceil(0.95×5)=5 and is 40 ms. The small sample does not tightly determine a population tail.

**Q5 (expansion). Can a kernel-only measurement legitimately exclude allocation?**

Yes, when it is labeled kernel-only and both candidates use the same boundary. An application comparison must separately account for allocation when the real application pays it.

**Written problems — worked guidance**

**P38.2-A. Durations are 2,3,3,4,8,10 ms after warmup. Compute mean, median and nearest-rank p95.**

Sum is 30 ms, mean is 5 ms, median is (3+4)/2=3.5 ms. p95 rank ceil(5.7)=6 gives 10 ms.

**P38.2-B. Variant B is 20% faster but skips one result in every 1,024. May its timings be accepted for an exact operation?**

No. It fails the exact-result contract. Repair the implementation or define and approve a different quality contract before comparing timings; do not relabel the bug as an optimization afterward.

**Published example output**

```json
{
  "status": "ok",
  "n": 3,
  "mean_ns": 20,
  "median_ns": 20,
  "p95_ns": 30,
  "excluded_warmup": 1
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 38.3 — SIMD, cache blocking, NUMA and job scheduling

**Q1 (original). What is false sharing?**

False sharing is interference when independently updated logical data share a coherence unit, causing ownership traffic. It is different from threads intentionally updating the same value.

**Q2 (original). Why can very small jobs be inefficient?**

Dispatch, queue, synchronization and bookkeeping costs can exceed their useful work. More jobs may also increase contention.

**Q3 (original). Why test small workloads after a parallel optimization?**

Small workloads reveal setup and scheduling costs hidden by large batches. An optimization can help throughput at large sizes while hurting typical interactive latency.

**Q4 (expansion). For ready costs 8,1,8,1 on two workers, compare round robin and greedy makespan with no overhead.**

Round robin produces loads 16 and 2, so makespan is 16. Greedy earliest-available placement produces 9 and 9, so makespan is 9.

**Q5 (expansion). Does changing to structure-of-arrays always improve performance?**

No. It depends on the fields consumed, access order, conversion cost and memory system. Measure the full consuming pipeline with the same useful result.

**Written problems — worked guidance**

**P38.3-A. Sixty-four jobs each perform 2 microseconds of work and pay 3 microseconds overhead. On one worker, what fraction of total time is overhead?**

Total is 64×5=320 microseconds; overhead is 64×3=192 microseconds. Overhead fraction is 192/320=60%.

**P38.3-B. In a hypothetical machine with 64-byte coherence lines, two 8-byte counters begin at offsets 0 and 8 of the same line. Is updating them independently sufficient to avoid false sharing?**

No. The addresses differ but share the same coherence line. Per-worker separated storage or a different reduction design may help; verify the actual platform and the footprint tradeoff.

**Published example output**

```json
{
  "loads": [16.0, 2.0],
  "makespan": 16.0,
  "total_service": 18.0
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 38.4 — Energy, thermal behavior and sustained performance

**Q1 (original). How much energy is 50 W for 2 seconds?**

100 joules, because 50 watts × 2 seconds = 100 joules.

**Q2 (original). Which example uses less task energy?**

The original 80 W for 1 second case uses 80 J, less than the 100 J used by 50 W for 2 seconds. This is task energy at the stated boundary, not a complete battery-life comparison.

**Q3 (original). Why not disable thermal protections for a curriculum benchmark?**

Protections are part of safe device operation. Disabling them can damage equipment or create hazards and invalidates the normal-use performance question. Use normal limits or synthetic traces.

**Q4 (expansion). Why distinguish interval-average from instantaneous power samples?**

Their integration assumptions differ. Interval-average power is multiplied by its interval directly; endpoint instantaneous samples require an interpolation or integration assumption.

**Q5 (expansion). Can lower watts mean worse efficiency?**

Yes. If useful work falls by a larger fraction than power, work per joule becomes worse. Report the output quality and useful-work boundary.

**Written problems — worked guidance**

**P38.4-A. Three interval-average samples are 20 W for 2 s, 30 W for 1 s and 10 W for 3 s. Find energy and average power over the full interval.**

Energy = 40+30+30 = 100 J. Total time is 6 s, so average power is 100/6 ≈ 16.667 W.

**P38.4-B. A system produces 1,200 accepted frames using 800 J. Another produces 1,000 using 500 J at the same quality. Compare frames per joule.**

First: 1.5 frames/J. Second: 2.0 frames/J. The second is more energy efficient by this metric, but latency and completion rate still need separate comparison.

**Published example output**

```json
{
  "joules": 100.0,
  "duration_s": 2,
  "average_w": 50.0,
  "frames_per_joule": 1.2
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Module 38 — Review answers

**R38-1. A kernel-only speedup is 8x but the kernel occupied 5% of a frame. Find the no-overhead additive frame speedup.**

Normalized time = 0.95 + 0.05/8 = 0.95625; speedup ≈ 1.04575x. New overhead or overlap can reduce benefit further.

**R38-2. Your fastest implementation fails only at N=17. How should performance results be handled?**

Reject results for the claimed exact contract until the tail or boundary bug is repaired. Preserve the rejected experiment and rerun validation and timing after the fix.

**R38-3. A parallel version wins at N=1,000,000 but loses at N=100. What should the report recommend?**

Report the distribution-dependent tradeoff, investigate setup/dispatch costs and evaluate a tested fallback threshold or coarser batching. Do not declare a universal winner from the large case alone.

**R38-4. A power trace uses endpoint instantaneous samples but the script treats them as interval averages. What must change?**

Correct the data contract or use a stated interpolation/integration model appropriate to the samples, such as a trapezoidal estimate. Recompute results and preserve the original provenance and correction.

**R38-5. A counter correlates with frame spikes. What additional work supports causality?**

Verify event meaning and timing scope, propose a mechanism, then manipulate the suspected cause under controlled workloads while validating output. Repeated correlation alone does not isolate the cause.


## Module 39 — Answers


### Lesson 39.1 — Input-to-display latency and frame pacing

**Q1 (original). Is 60 frames per second a complete latency measurement?**

No. It describes average throughput, not the age of the input used, queueing delay, interval consistency or display response.

**Q2 (original). What is two 60 Hz frame intervals?**

Approximately 33.333 milliseconds: 2 × (1000/60) ms.

**Q3 (original). Why label timestamp boundaries precisely?**

The interpretation of a latency depends on the events, clock domains and scopes used. A presentation marker is not automatically a photon timestamp.

**Q4 (expansion). Which is correct for throughput: reciprocal of mean interval or mean of interval reciprocals?**

For total completions over elapsed time, use reciprocal of the mean interval, with units handled consistently. Averaging individual reciprocal intervals answers a different question.

**Q5 (expansion). A trace measures input to software presentation callback. Can it establish panel response time?**

No. Panel response is outside that boundary. Label it input-to-callback and use a separate physical method for optical stages.

**Written problems — worked guidance**

**P39.1-A. Input occurs at 8 ms and the software presentation marker at 42 ms. The panel response is unmeasured. What latency may be reported?**

Input-to-software-marker latency is 34 ms. Total input-to-photon latency and panel response cannot be determined from these timestamps.

**P39.1-B. Presentation intervals are 10,10,40 ms. Find total-throughput FPS and compare it with the arithmetic mean of interval FPS.**

Mean interval is 20 ms, giving 50 FPS. Individual reciprocals are 100,100,25 FPS, averaging 75 FPS; that does not equal total frames per elapsed time.

**Published example output**

```json
{
  "mean_latency_ms": 20,
  "p95_latency_ms": 20,
  "min_interval_ms": 10,
  "max_interval_ms": 10,
  "mean_rate_fps": 100.0,
  "boundary": "synthetic_present"
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 39.2 — Mobile and handheld systems: memory, power and lifecycle

**Q1 (original). Why not assume shutdown always provides unlimited save time?**

The process can be terminated without unlimited callback time, and a last-minute save can fail. Persist progress under a documented checkpoint and recovery policy during normal operation.

**Q2 (original). Why measure sustained rather than only initial performance?**

Initial results may not represent later thermal, power or resource conditions. Sustained work reveals behavior relevant to longer sessions.

**Q3 (original). What should rendering quality tiers preserve?**

Gameplay and simulation correctness, the declared useful visual-quality floor, and supported accessibility behavior. Optional rendering work may be reduced under a tested policy.

**Q4 (expansion). After checkpointing tick 10, advancing to tick 17 and receiving a sudden kill, what does the model restore?**

Tick 10. Ticks 11–17 were not checkpointed. The model does not invent a graceful-save callback.

**Q5 (expansion). Why attach a generation to recreated rendering resources?**

It prevents stale handles from an earlier lifetime from being accepted as current after suspension, destruction or recreation.

**Written problems — worked guidance**

**P39.2-A. A budget is 512 MiB. Persistent state is 260 MiB; current and replacement resource sets each need 140 MiB. Can both coexist?**

Peak is 260+140+140=540 MiB, which exceeds the budget by 28 MiB. Steady state at 400 MiB does not make the transition safe.

**P39.2-B. A save claims version 9 but the loader supports versions 1–3. What is a defensible response?**

Reject or enter an explicitly supported recovery/migration path. Do not reinterpret an unknown layout as version 3 or silently overwrite the only recoverable save.

**Published example output**

```json
{
  "state": "RUNNING",
  "tick": 2,
  "saved_tick": 0,
  "resources_live": true,
  "generation": 1
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 39.3 — XR spaces, stereo views, pose timing and comfort constraints

**Q1 (original). Why is a pose incomplete without a space and time?**

Without a reference space and timestamp, the transform cannot be composed or interpreted reliably. Units and coordinate conventions are also required.

**Q2 (original). Should stereo projection be hard-coded for every headset?**

No. Use the runtime-provided per-view geometry and projection information for the selected configuration. A teaching symmetric camera pair is not every headset.

**Q3 (original). Does prediction remove all latency or discomfort risk?**

No. Prediction is an estimate with motion and timing assumptions; tracking errors and display latency remain, and comfort varies. It cannot guarantee freedom from discomfort.

**Q4 (expansion). Why is the view translation -R^T p rather than simply -p?**

The inverse transform must express the translated point in the inverse-rotated camera basis. Inverting rotation and translation requires the composed rigid-transform inverse.

**Q5 (expansion). At 1 m/s over a 20 ms prediction interval, what translation is predicted?**

0.02 m, or 2 cm, under constant velocity. This says nothing about acceleration error or actual display timing.

**Written problems — worked guidance**

**P39.3-A. Constant speed is 0.5 m/s and prediction horizon is 30 ms. Find predicted displacement.**

0.5×0.030 = 0.015 m, or 1.5 cm. The prediction assumes constant velocity over that horizon.

**P39.3-B. A camera at world position (2,0,0) has identity rotation. Where does world point (2,0,-3) appear in camera coordinates?**

Subtract camera position, giving (0,0,-3). With identity rotation no further rotation is needed; it is three meters forward under the -Z-forward convention.

**Published example output**

```json
{
  "render": "stereo_model",
  "left_m": [-0.032, 0, 0],
  "right_m": [0.032, 0, 0],
  "prediction_s": 0
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 39.4 — Portability, platform services and console-development boundaries

**Q1 (original). Why can a strict mock help portability?**

A strict mock rejects unsupported behavior, permissions and lifecycle assumptions early. An always-successful mock hides the very constraints that portability work needs to expose.

**Q2 (original). Does public self-study grant access to proprietary console SDKs?**

No. Public self-study does not provide proprietary SDK access, credentials, agreements or platform certification.

**Q3 (original). Why separate packaged assets from persistent saves?**

Installed assets and persistent saves have different permissions and lifetimes. Use supported writable storage for saves rather than assuming the installation directory can be modified.

**Q4 (expansion). What should happen when a required capability is missing?**

Fail or enter an explicitly specified supported fallback mode. Do not claim successful initialization while silently dropping a required behavior.

**Q5 (expansion). Does successful capability negotiation prove the backend is correct?**

No. It checks advertised support. Behavioral tests must verify permissions, failures, lifecycle and actual implementation semantics.

**Written problems — worked guidance**

**P39.4-A. Required features are render/save; available features are render/haptics. Is startup allowed by the contract?**

No. Save is required and missing. Haptics does not substitute for a required storage capability.

**P39.4-B. A mock returns success for a save to a read-only packaged-asset path. What test is missing?**

A permission-boundary test that rejects writes to packaged assets and requires the writable persistent-storage route. Also test that the game reports or recovers from that rejection rather than losing data silently.

**Published example output**

```json
{
  "accepted": true,
  "missing": [],
  "enabled_optional": ["ray"]
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Module 39 — Review answers

**R39-1. Two engines average 60 FPS; one reports much older input at presentation. Explain a likely distinction.**

Queue depth, simulation buffering or input-consumption timing can differ despite identical throughput. Compare input-to-named-marker distributions and stage timelines; optical latency requires additional measurement.

**R39-2. A quality change fits steady memory but fails during recreation. What budget was omitted?**

Peak transitional memory, including old/new resources, staging, decompression and temporary allocations. Test the transition, not only the settled tier.

**R39-3. Stereo looks correct at zero yaw but eye positions are wrong after a turn. Identify a likely transform bug.**

Eye offsets may have been applied in world X instead of rotating local eye offsets with the head pose. Verify conventions with known 90-degree rotations and inverse-view tests.

**R39-4. A save service disappears after capability negotiation. What should a robust engine do?**

Use the current service/lifecycle contract, retain or cancel pending work safely, report a defined failure and recover or fallback without falsely acknowledging durable progress. Startup negotiation is not a permanent guarantee.

**R39-5. List the boundaries a platform report must avoid overstating.**

A simulated presentation timestamp is not photon timing; a pose test is not an XR comfort guarantee; a capability mock is not console certification; a symbolic checkpoint is not production storage durability.


## Module 40 — Answers


### Lesson 40.1 — Workload characterization and measurable requirements

**Q1 (original). Why start with workload measurements?**

To identify an important operation, its actual input distribution, timing contribution, constraints and quality requirements. Without those, an accelerator may optimize work that does not matter to the application.

**Q2 (original). What maximum fraction of the example frame can removing 0.2 ms save?**

At most 1% of frame time under the stated additive model: 0.2/20=0.01. Remaining time is 19.8 ms and maximum speedup is approximately 1.0101x.

**Q3 (original). Can rejecting a hardware proposal be a successful outcome?**

Yes. Rejecting an architecture on rigorous workload, quality or end-to-end evidence is a valid engineering outcome.

**Q4 (expansion). Why is a Python correctness oracle not automatically a competent performance baseline?**

It may use a different execution environment and implementation strategy from the target engine. Keep oracle correctness evidence separate from a suitably optimized target baseline.

**Q5 (expansion). What should a performance requirement specify besides a number?**

Metric, units, timing boundary, workload distribution, numerical or visual quality, test method and relevant operating conditions.

**Written problems — worked guidance**

**P40.1-A. An operation takes 3 ms in a 15 ms frame. It improves 3x but adds 0.4 ms setup/transfer. Find new frame time and speedup.**

New frame time = 15−3+3/3+0.4 = 13.4 ms. Speedup = 15/13.4 ≈ 1.1194x; time saving is 1.6/15 ≈ 10.667%.

**P40.1-B. A subsystem consumes 4 ms of CPU time but fully overlaps an independent 7 ms GPU path. Does removing all 4 ms necessarily save 4 ms of frame time?**

No. If both start together and the final result waits on the 7 ms path, that path still sets completion. Dependencies, start times and later work must be analyzed before claiming a saving.

**Published example output**

```json
{
  "maximum_saved_fraction": 0.01,
  "new_frame_ms": 19.9,
  "application_speedup": 1.0050251256281408
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 40.2 — Architecture alternatives, arithmetic precision and dataflow

**Q1 (original). Why might twice as many lanes fail to double throughput?**

Memory bandwidth, setup, dependencies, control overhead or another resource may limit throughput. Extra lanes help only when work and data can reach them.

**Q2 (original). What should determine acceptable quantization error?**

The application’s numerical, visual or gameplay-quality requirements, dynamic range and worst-case error tolerance, not simply the narrowest representation that passes average inputs.

**Q3 (original). Why explore more than one architecture?**

To expose different bottlenecks and tradeoffs rather than assuming the first implementation is best. Compare credible alternatives with the same useful result and boundary.

**Q4 (expansion). What is the maximum representable signed Q8.8 value?**

32767/256 = 127.99609375. The minimum is −32768/256 = −128.

**Q5 (expansion). What does the pipeline model’s clock assumption prove about physical timing?**

Nothing by itself. The assumed frequency converts declared model cycles into estimates; it is not synthesis, timing closure or physical measurement.

**Written problems — worked guidance**

**P40.2-A. Eight groups pass through an initiation-interval-one model with latency four cycles and no stalls. What is first-acceptance to last-retirement elapsed time?**

4+8−1=11 cycles. If a trace samples both endpoint ticks, it contains 12 tick positions. State which quantity is being reported.

**P40.2-B. An operation moves 8 bytes/item at a declared 240 MB/s. What is its bandwidth-limited item rate, ignoring other costs?**

240,000,000/8 = 30,000,000 items/s. Extra compute lanes cannot exceed this rate without changing traffic or bandwidth.

**Published example output**

```json
{
  "raw": [-256, 0, 256, 32767],
  "saturated": 0
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 40.3 — Interface design, virtualization and end-to-end evaluation

**Q1 (original). Why validate device work descriptors?**

To prevent unsupported operations, invalid formats, out-of-range or misaligned access, wrong-context access and ownership violations. Descriptor validation is part of correctness and isolation.

**Q2 (original). Can kernel and application speedups legitimately differ?**

Yes. Setup, transfers, synchronization, result consumption and unchanged application work can dominate outside the kernel. Each speedup must state its boundary.

**Q3 (original). Why test realistic batch sizes?**

Actual game batches determine whether setup is amortized and whether resources are filled. Large synthetic batches can conceal a loss on normal interactive workloads.

**Q4 (expansion). Does increasing an epoch make a timed-out DMA buffer physically safe to reuse?**

No. It rejects stale logical completions but does not stop old hardware accesses. Reuse requires confirmed completion or a quiescent cancellation/reset policy.

**Q5 (expansion). Why prefer count <= (size-offset)/stride after validating offset?**

It avoids overflow in computing offset + count×stride in fixed-width arithmetic, while expressing the remaining-buffer bound directly.

**Written problems — worked guidance**

**P40.3-A. A 1,024-byte buffer uses 4-byte elements. Offset is 1,000 and count is 7. Is the request valid?**

Remaining capacity is 24 bytes or 6 elements, so count 7 is invalid. Count 6 exactly fits, assuming offset alignment and other checks pass.

**P40.3-B. CPU time is 0.3 microseconds/item; an alternative costs 15 microseconds setup plus 0.1 microseconds/item. Find the first integer batch size that wins.**

15+0.1N < 0.3N implies N>75. At N=75 the times tie; the first winning integer size is 76, under the stated complete boundary.

**Published example output**

```json
{
  "statuses": ["submitted", "completed"],
  "owner": "HOST",
  "epoch": 0,
  "pending": false,
  "quarantined": false
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Lesson 40.4 — Design review, evidence tiers and undergraduate CE completion

**Q1 (original). Why label simulation and physical measurements separately?**

They establish different facts and have different assumptions. A simulation can be correct under its model without proving physical timing, power, signal integrity or device behavior.

**Q2 (original). What makes a baseline competent?**

An appropriate algorithm and implementation for the target, suitable build settings and layout, correct useful results, fair batching and timing boundaries, and consideration of credible existing alternatives.

**Q3 (original). Does Gate H authorize production chip fabrication?**

No. Gate H is a self-study engineering checkpoint, not a degree, professional authorization, tape-out signoff or production fabrication approval.

**Q4 (expansion). Does a matching file hash prove an experiment is scientifically sound?**

No. It identifies file contents and detects changes. It does not establish correctness, fairness, completeness or valid inference.

**Q5 (expansion). May a well-supported negative result pass Gate H?**

Yes. The objective is a defensible engineering decision supported by the required implementation, tests, comparison and evidence, not a mandatory speedup.

**Written problems — worked guidance**

**P40.4-A. A cycle model predicts 12 microseconds at an assumed clock. A host benchmark measures 18 microseconds for a different implementation. Can the report claim a measured 1.5x hardware speedup?**

No. It may report a conditional modeled ratio 18/12=1.5 under a carefully matched useful-work boundary, but the accelerator time is not measured hardware evidence and the implementations/overheads must be reconciled.

**P40.4-B. The main dataset changes after hashes are recorded. What should the evidence workflow do?**

Reject the stale hash, preserve or version the old artifact, rerun affected tests and summaries, update the ledger and record the change. Do not silently replace the hash while retaining conclusions from different inputs.

**Published example output**

```json
{
  "issues": [],
  "structurally_complete": true
}
```

Compare this with your prediction, then inspect the reference implementation and add a case that distinguishes your reasoning from a plausible incorrect implementation.


### Module 40 — Review answers

**R40-1. What minimum alternatives and evidence are required by Gate H?**

A measured engine workload, competent software baseline and at least two architecture alternatives; implement one in RTL, supported simulation or a bounded analytical prototype. Include quality, ownership, end-to-end costs, resource/timing estimates, failures, small/large/adverse cases and sensitivity.

**R40-2. Four lanes produce no gain over one in the supplied model. Explain the asymptotic limit.**

Four bytes/item at 400 MB/s gives 100 million items/s. A one-lane 100 MHz initiation-interval-one model already approaches that rate, so internal bandwidth prevents asymptotic compute-lane scaling under these assumptions.

**R40-3. A timed-out request resets its software epoch, but old hardware is still writing. Is isolation restored?**

No. Epochs reject stale completions but cannot stop memory accesses. Confirm device quiescence and preserve buffer ownership before reuse; real multi-context isolation needs additional supported mechanisms.

**R40-4. A model’s assumed 100 MHz clock is accidentally labeled measured. How should the review respond?**

Correct the evidence tier and conditional wording, audit derived timing claims and document the change. Obtain actual implementation/timing evidence before making a physical-frequency claim.

**R40-5. An accelerator loses to improved software on every representative batch. Can the capstone pass?**

Yes, when the baseline is fair, the specialized implementation and alternatives are genuinely evaluated, all required tests/evidence are present and the negative conclusion explains the bottleneck and sensitivity. Merely guessing it will lose is not enough.


## Assessing design and transfer work
For the full labs, require the original acceptance criterion, the named evidence and a reproducible demonstration. Reward an independently justified alternative rather than insisting on the reference model's chosen architecture. Do not award completion for a JSON checker when the original assignment requires a schematic, engine experiment or strict backend.

For transfer tasks, check that the changed condition is precisely defined, a prediction is made, the implementation or derivation tests it and the result is interpreted within its boundary. A negative result can be correct. Unsupported claims about real hardware, optical latency or a manufacturing-ready design are not acceptable substitutes for missing evidence.

Gate H decisions are assessed with CAPSTONE_SPEC. The teaching reference's scripts and results are visible so the workflow can be studied, but copying them without the required measured engine workload and review does not complete the learner capstone.
