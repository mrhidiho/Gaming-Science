# Volume 10 Answer Key

**Sixty explained lesson answers · Twenty lab-review notes · Ten transfer solutions**

## How to use this key

Keep this file separate during first attempts. A correct answer should explain why the conclusion follows and where it stops applying. Wording need not match the key. Give credit for a technically sound alternative with explicit assumptions, but not for a broader claim unsupported by its evidence.

The lab notes are reviewer guidance, not fabricated student completion records. They describe expected reasoning and known fixture results. A lab that requires an actual tool run, independent reviewer or thesis artifact cannot be completed by copying the note. Review the original pass condition in the workbook.

A proposed quiz mastery check is two correct answers plus a repaired explanation of the third. Repeated errors about undefined behavior, timing exceptions, vacuity, fault guarantees or research integrity should trigger prerequisite repair even when the numerical score looks acceptable.


# Module 46 answer key
## Advanced computer architecture for gaming workloads

## Lesson 46.1 — Cache coherence, memory consistency and synchronization

**46.1.Q1** After A writes seven while B holds a shared copy, what ownership condition must hold before A is considered Modified?

**Expected reasoning:** B must be invalidated and exclusive permission established. In an asynchronous implementation, pending invalidation acknowledgments require a transient state; granting M before exclusivity is established is unsafe.

**46.1.Q2** Why is a coherent cache system insufficient justification for a C++ producer using a relaxed ready flag with a non-atomic payload?

**Expected reasoning:** Coherence does not supply the required language-level happens-before relation. A release store and an acquire load that observes it can publish the preceding payload write. A relaxed flag alone does not establish that relation; conflicting non-atomic accesses can be a data race.

**46.1.Q3** Under sequential consistency, why is the zero/zero store-buffering outcome impossible, and why is “not observed” weaker than “forbidden”?

**Expected reasoning:** The two program-order edges plus the read-before-other-store requirements form a cycle in a proposed total order. A finite run samples executions; it cannot exclude an allowed but rare execution.

### Lab 46.1 review guidance
The six-operation trace ends with both caches Shared at nine and memory nine. Reads return zero, zero, seven and nine in order. The deliberate invalidation omission must be caught either by M-versus-S ownership or by a later stale read. The bundled enumeration validates atomic transitions only; acceptance also requires the separately reasoned transient cases. No sampled C++ execution establishes a universal weak-memory theorem.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 46.2 — Out-of-order execution, speculation and precise state

**46.2.Q1** Which dependencies can register renaming remove, and which dependency must remain?

**Expected reasoning:** Renaming can remove WAR and WAW name dependencies by assigning distinct physical destinations. A RAW dependency supplies a required value and remains.

**46.2.Q2** In the worked four-instruction example, why can earlier completion of C and D fail to reduce total retirement time?

**Expected reasoning:** In-order retirement and retirement width one serialize A, B, C and D after the oldest results become available. Completion overlap is not automatically a reduction in the critical retirement path.

**46.2.Q3** If B faults after C has completed, which results may appear in precise architectural state?

**Expected reasoning:** Only effects older than B, here A, may be committed. B and younger C/D cannot be architectural, even if they finished execution.

### Lab 46.2 review guidance
The supplied four-instruction, width-one model retires the last instruction at cycle seven under both policies. Tests should compare the full committed dictionary. An exception at B leaves only A committed. A window of one collapses out-of-order freedom. Do not interpret the tested instruction DAG as a cache-accurate CPU or claim modeled cycle counts are physical measurements.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 46.3 — Architecture simulation, traces and model validation

**46.3.Q1** Why does changing from two direct-mapped sets to two two-way sets fail to isolate associativity?

**Expected reasoning:** It changes capacity from two to four lines as well as associativity. Hold total lines constant, or explicitly describe both factors changing.

**46.3.Q2** Under the additional-miss-penalty convention, what is the modeled cost for N=100, M=10, h=2 and p=30?

**Expected reasoning:** 100*2 + 10*30 = 500 modeled serial cycles. If 30 were the entire miss cost, the result would instead be 480; the convention must be recorded.

**46.3.Q3** How do verification, calibration and validation differ in an architecture study?

**Expected reasoning:** Verification checks implementation against specification; calibration estimates parameters; validation tests predictive usefulness against separate evidence. Reusing calibration observations as validation overstates independence.

### Lab 46.3 review guidance
The worked direct-mapped trace has four misses; the two-way, same-set-count trace has three. Equal-capacity comparisons are required before attributing the difference solely to associativity. A serial-cycle model must count lookup cost on every request under the documented additional-penalty convention. Real machine prediction remains unvalidated unless the learner adds independent measurement.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 46.4 — Memory systems, chiplets and multi-objective design

**46.4.Q1** Which of A, B, C and D is dominated in the worked example, and by which design?

**Expected reasoning:** C is dominated by A: 10<12 ms, 40<45 W and 20<22 area units. A, B and D trade objectives and remain on the point-estimate frontier.

**46.4.Q2** Why does a 42 W/24-area constraint select A, while a 42 W/26-area constraint can select D?

**Expected reasoning:** B exceeds the power ceiling, C is slower/dominated and exceeds power, and D initially exceeds area. With area 26, D becomes feasible and wins under a minimum-latency policy.

**46.4.Q3** What information is missing when someone uses peak link bandwidth alone to predict frame latency?

**Expected reasoning:** Fixed and queueing latency, request dependencies, usable rather than signaling bandwidth, burstiness, contention, transfer sizes, protocol traffic and the workload critical path are missing.

### Lab 46.4 review guidance
The frontier is A/B/D. The required constraint-change example selects A then D. Equal vectors remain non-dominated under strict dominance. Unknown power or area must be recorded as unknown or a labeled assumption, not fabricated from modeled cycles. A recommendation can be correct even when it changes under a new constraint.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

# Module 47 answer key
## VLSI, timing and physical implementation

## Lesson 47.1 — CMOS logic, transistor sizing and delay models

**47.1.Q1** Why can increasing an output gate’s drive strength worsen the complete path?

**Expected reasoning:** The larger gate adds input capacitance to the preceding stage, and may add parasitic capacitance and power. The complete path and interface load must be included.

**47.1.Q2** For H=64 and p=1, what is the three-stage equal-effort delay and what are the normalized sizes?

**Expected reasoning:** Each effort is four, so D=3*(4+1)=15. With first-stage input one and final load 64, sizes are 1,4,16. Three inversions invert polarity.

**47.1.Q3** Why is a delay reported in normalized units not a measured nanosecond delay?

**Expected reasoning:** The normalization lacks characterized physical constants and corner-specific slew/load behavior. A conversion needs a valid technology model or measured calibration, not an assumed clock rate.

### Lab 47.1 review guidance
For N=1..4 the modeled delays are 65,18,15,approximately15.314. The three-stage choice assumes inversion is permitted. No claim of library agreement is accepted without actual characterized data or a recorded simulation. The normalized calculation and input-loading discussion can be reviewed before external tools are available.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 47.2 — Static timing analysis, clocks and timing exceptions

**47.2.Q1** Using the worked values, what are setup and hold slack at T=2.0 ns?

**Expected reasoning:** Setup is +0.25 ns. Hold is −0.06 ns. At T=1.6 ns setup becomes −0.15 ns and the simple hold slack remains −0.06 ns.

**47.2.Q2** With positive skew defined as capture minus launch arrival, why does positive skew help setup but hurt hold?

**Expected reasoning:** The next capture edge moves later, giving new data more setup time. The same-edge hold window also moves later, requiring old data to remain stable longer.

**47.2.Q3** Why is “zero violations” insufficient when assessing a timing report?

**Expected reasoning:** Unconstrained endpoints, missing clocks, incorrect corner assumptions or unjustified false paths can eliminate required checks. Coverage and exceptions must be audited alongside slack.

### Lab 47.2 review guidance
The reference calculation must reproduce +0.25/−0.06 ns and show setup dependence on period with unchanged simple hold slack. The SDC is an educational environment contract, not a board-derived constraint set. Actual STA reports are learner-generated; the arithmetic demonstration alone cannot satisfy the external timing-flow requirement.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 47.3 — Synthesis, placement, clock trees, routing and physical checks

**47.3.Q1** Why should a FIFO’s full-and-simultaneous-pop behavior be fixed before comparing implementations?

**Expected reasoning:** It is part of the accepted-transaction/throughput contract. Different acceptance rules can change useful work and latency, invalidating a supposedly like-for-like physical comparison.

**47.3.Q2** Why can the worst setup slack change after routing without a change in RTL function?

**Expected reasoning:** Wire parasitics, buffering and clock paths become more concrete; the critical path may also change. Logical equivalence and timing are different properties.

**47.3.Q3** What does producing a GDS file fail to establish?

**Expected reasoning:** It does not by itself establish functional correctness, complete DRC/LVS, timing closure, power integrity, manufacturing approval, licensing clearance or commercial signoff.

### Lab 47.3 review guidance
Acceptance requires either the learner’s actual educational flow or a reviewed, explicitly attributed official example inspection as allowed by the manifest. This package does not include generated physical reports. Any synthetic lesson numbers must remain synthetic. The FIFO blocks a push when already full even if a pop occurs on that edge.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 47.4 — Power, area, process corners and design-space closure

**47.4.Q1** Compute the dynamic-power estimate for alpha=0.2, C=10 pF, V=1 V and f=100 MHz.

**Expected reasoning:** 0.2*10e-12*1^2*100e6=0.0002 W=0.2 mW under the stated charging-event convention.

**47.4.Q2** Why can a 3 mW design be more energy-efficient than a 2 mW design?

**Expected reasoning:** Energy per item is power divided by useful throughput. At 2 million items/s, 3 mW is 1.5 nJ/item; at 1 million items/s, 2 mW is 2 nJ/item. A hard power limit can still reject the former.

**47.4.Q3** What must be held constant or disclosed when comparing PPA for two RTL implementations?

**Expected reasoning:** Functional contract, workload, precision, clock and I/O constraints, platform/library/corners, tool revisions, area definition, activity coverage and estimation assumptions must match or be explicitly accounted for.

### Lab 47.4 review guidance
The numerical checks are 0.2 mW at 1 V and 0.128 mW at 0.8 V under unchanged frequency and activity. Those calculations alone do not demonstrate lower-voltage timing feasibility. Actual PPA comparison requires learner-generated reports. Do not substitute the package’s synthetic frontier table for physical implementation evidence.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

# Module 48 answer key
## Verification, reliability and hardware trust boundaries

## Lesson 48.1 — Formal properties, abstraction and assume-guarantee reasoning

**48.1.Q1** Why does occupancy staying in range fail to prove FIFO ordering?

**Expected reasoning:** An implementation can maintain the correct number of entries while returning the wrong entry, such as LIFO order or a duplicate. Ordering needs a data property or reference relation.

**48.1.Q2** What is the difference between a depth-20 bounded pass, an unbounded proof under assumptions, and a timeout?

**Expected reasoning:** A bounded pass excludes counterexamples only within the checked depth/model. An unbounded proof establishes the property for all modeled reachable time under its assumptions. A timeout is unknown, not a pass.

**48.1.Q3** How can a cover goal and a deliberately injected bug expose a vacuous property?

**Expected reasoning:** A cover checks that the triggering situation is reachable. A bug that should violate the property must produce a failure; otherwise assumptions, activation or the property itself may exclude the relevant behavior.

### Lab 48.1 review guidance
The two-value, capacity-two abstract sequence space has seven states: empty, two one-item states and four two-item states. Reaching all seven is not proof of arbitrary RTL widths. The full-write mutation must be rejected by range/accounting checks; a LIFO mutation requires ordering checks. Optional formal tasks may remain not-run if tools are absent, but cannot be described as passed.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 48.2 — Clock/reset crossings and asynchronous FIFO verification

**48.2.Q1** Why must the source hold mailbox data stable until the acknowledgment returns?

**Expected reasoning:** The destination captures the multi-bit payload after the request crosses. Overwriting it early can associate the event with a later or mixed payload. The acknowledgment establishes completion before reuse.

**48.2.Q2** Why does Gray-coding a FIFO pointer not eliminate the need for physical CDC constraints?

**Expected reasoning:** Gray coding limits changes between adjacent source values, but inter-bit routing skew and synchronization behavior still affect what is sampled. Digital protocol correctness is not analog metastability or implementation signoff.

**48.2.Q3** What guarantee does the reference handshake make across a coordinated reset, and why is unilateral reset rejected?

**Expected reasoning:** It flushes in-flight data and starts a new explicitly labeled epoch; it does not guarantee delivery across reset. Resetting only one toggle can create false or lost events without a resynchronization protocol.

### Lab 48.2 review guidance
The mailbox can hold at most one unacknowledged item. Accepted order and delivered order must match after draining within an uninterrupted epoch. Backpressure may delay progress but must not change the stored payload. Coordinated reset intentionally drops in-flight work; tests must not count that as unexplained loss or promise it is preserved. No simulation result here establishes a numerical MTBF.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 48.3 — Fault models, ECC, testability and recovery

**48.3.Q1** What do syndrome nonzero and even overall parity mean under the SECDED fault model?

**Expected reasoning:** It is the double-error-detected case. The decoder must not present the payload as trusted corrected data; the recovery policy should handle an uncorrectable word.

**48.3.Q2** How many single-bit and double-bit cases must be tested over all sixteen four-bit payloads?

**Expected reasoning:** 16*8=128 single-bit cases and 16*C(8,2)=448 double-bit cases, plus 16 clean words.

**48.3.Q3** Why can a triple-bit error be miscorrected despite a correct SECDED implementation?

**Expected reasoning:** The supported guarantee is limited to one-bit correction/two-bit detection. A three-bit pattern can produce the same syndrome and overall parity as a single error, so the decoder may flip another bit and produce the wrong valid codeword.

### Lab 48.3 review guidance
Payload ten encodes as 0xD2 with positions counted from the least-significant bit. All 128 singles correct and all 448 doubles detect. One useful triple counterexample flips positions 1,2,3 of an all-zero codeword: syndrome is zero but overall parity is odd; treating this as an overall-parity-bit error yields incorrect payload one. Do not label that result “triple-error correction.”

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 48.4 — Hardware security, thermal limits and assurance review

**48.4.Q1** Why is length <= capacity−offset preferable to blindly checking offset+length <= capacity on a fixed-width machine?

**Expected reasoning:** After validating offset within range and nonnegative inputs, subtraction avoids overflow in the sum. Types, alignment and ownership still need separate validation.

**48.4.Q2** What does an epoch/generation check prevent after reset, and what does it not undo?

**Expected reasoning:** It rejects stale work or completions from a previous generation. It cannot undo partial writes or external effects already performed before reset.

**48.4.Q3** Why does a passing Python descriptor test not establish real DMA isolation or safe thermal operation?

**Expected reasoning:** The model omits device mappings, IOMMU configuration, hardware faults and physical heat transfer. Those require separate authorized implementation and measurement evidence.

### Lab 48.4 review guidance
The 4080/16 descriptor fits a 4096-byte aligned region; 4080/32 fails. Wrong owner and old generation fail independently of range. After reset, pending work is cleared and the generation advances. The synthetic thermal result is 70 C, not a universal device limit. No real DMA or hardware fault injection is performed by the bundle.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

# Module 49 answer key
## Master's thesis: proposal, implementation and evaluation

## Lesson 49.1 — Question selection, literature map and thesis scope

**49.1.Q1** What five elements make a broad “better hardware” topic into a testable thesis question?

**Expected reasoning:** A mechanism/intervention, defined workload/population, comparator, measurable outcome and stated constraints/fidelity boundary are essential; a refutation condition makes the test sharper.

**49.1.Q2** How can a reproduction or negative result still be a defensible contribution?

**Expected reasoning:** A careful reproduction establishes what can actually be regenerated, and a well-controlled negative result can identify limits or refute an expected gain. Both require rigorous baselines, transparent evidence and accurately bounded novelty.

**49.1.Q3** Why should the literature map include a source that challenges the proposal’s assumptions?

**Expected reasoning:** It exposes prior counterexamples, confounders and established limitations before expensive work. A map containing only supportive abstracts risks an uninformative or already-refuted study.

### Lab 49.1 review guidance
There is no single correct topic. Acceptance depends on a falsifiable question, a relevant baseline, a feasible evidence path and honest scope. The package’s synthetic command-queue example is only a worked framing aid; the learner must select and review their own sources. A proposal whose only success condition is “build something impressive” needs revision.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 49.2 — Proposal review, baselines and risk-reduction milestones

**49.2.Q1** Why is a working baseline with a correctness oracle more valuable than a large unvalidated prototype at the first milestone?

**Expected reasoning:** It establishes that the comparator and measurement path can test the question. Without it, a prototype can produce impressive but uninterpretable performance numbers.

**49.2.Q2** For 20 scenes, 3 configurations, 10 runs and 5 minutes per run, what is the execution budget?

**Expected reasoning:** 20*3*10*5=3000 minutes=50 hours, excluding setup, compilation, analysis, retries and failures.

**49.2.Q3** What distinguishes a legitimate protocol amendment from changing the question to fit results?

**Expected reasoning:** A legitimate amendment is versioned, justified and reviewed, with its timing relative to observed data disclosed. Post-hoc metric or workload changes must be labeled exploratory rather than presented as prespecified confirmation.

### Lab 49.2 review guidance
The worked run matrix is 50 execution hours. A good baseline can expose a failed assumption and legitimately cause a proposal revision. A risk register without triggers or decisions is incomplete. No candidate performance claim is accepted before equal work and measurement boundaries are established.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 49.3 — Implementation, ablations and controlled evaluation

**49.3.Q1** How does an ablation differ from a sensitivity study?

**Expected reasoning:** An ablation removes a component to isolate its contribution. A sensitivity study varies a parameter or assumption to test robustness. They answer different causal and stability questions.

**49.3.Q2** If baseline time is 10 ms and candidate time is 8 ms, what are speedup and time reduction?

**Expected reasoning:** Speedup is 10/8=1.25x; time reduction is (10−8)/10=20%. At equal work this corresponds to 25% higher throughput, not 25% less time.

**49.3.Q3** Why is resampling thousands of frames from one run not equivalent to collecting thousands of independent runs?

**Expected reasoning:** Frames share state, scene, thermal conditions and execution history. Dependence means the effective information differs from independent runs; the resampling unit must match the study design.

### Lab 49.3 review guidance
The four-pair geometric mean is approximately 1.206, to be checked by the executable implementation. Identical 1.25 ratios produce a degenerate bootstrap interval of 1.25 and provide a useful deterministic test. Such a test validates code arithmetic, not statistical generalization. Real thesis conclusions must use actual study data and matched independent units.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 49.4 — Thesis writing, reproducibility and contribution boundaries

**49.4.Q1** What is the purpose of a claim-to-evidence ledger?

**Expected reasoning:** It connects each exact claim to assumptions, raw evidence, generating commands, output and limitations, allowing an independent reviewer to audit the argument.

**49.4.Q2** Why does a matching SHA-256 file manifest not prove that a research conclusion is correct?

**Expected reasoning:** A hash comparison establishes byte consistency relative to the manifest. It does not establish trusted origin, absence of methodological error, valid statistics or correctness of the claimed inference.

**49.4.Q3** How should reproduction criteria differ between a deterministic cache count and a cross-machine timing experiment?

**Expected reasoning:** Deterministic counts can require exact equality. Cross-machine timing needs prespecified numerical/statistical criteria and environment disclosure; identical absolute times may be inappropriate.

### Lab 49.4 review guidance
Acceptance is evidence-based rather than page-count-based. Every central claim must match its evidence tier and have a runnable path. A hash manifest with fabricated data is still invalid research; reviewers check provenance and method. The package’s reference examples are not a substitute for the learner’s own thesis artifact.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

# Module 50 answer key
## Thesis defense, professional practice and continued development

## Lesson 50.1 — Oral defense and independent artifact reproduction

**50.1.Q1** Why is a second run by the author on the same prepared machine not independent artifact reproduction?

**Expected reasoning:** It does not test whether another person can operate the release from its documented entry point without hidden setup or author-specific knowledge. It remains useful internal validation.

**50.1.Q2** What should happen when a reviewer cannot reproduce the central ranking?

**Expected reasoning:** Preserve both runs, investigate identities and methodology, record the discrepancy and require revision. Narrow or suspend the affected claim until supported; do not discard the reviewer’s result.

**50.1.Q3** Can a favorable average result override a violated hard correctness or adverse-case requirement?

**Expected reasoning:** No. Hard constraints are gates. A bounded negative finding can still be a valid thesis contribution, but the original acceptance claim must be revised honestly.

### Lab 50.1 review guidance
Passing requires actual reviewer evidence and completed blocking revisions. A self-score or this bundle’s reference test report cannot substitute for independent thesis reproduction. The suggested 40-minute structure is one workable schedule within the manifest’s 30–45 minute range.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 50.2 — Mature-codebase integration, review and maintainable contributions

**50.2.Q1** Why should a performance patch include correctness and adverse-case evidence?

**Expected reasoning:** An apparent speed gain can result from changed work or broken outputs, and representative averages can hide unacceptable regressions. The patch must preserve the required contract.

**50.2.Q2** What is the strongest basic evidence for a bug-fix regression test?

**Expected reasoning:** The test fails for the intended reason on the base revision and passes with the patch, with enough context to exclude unrelated environmental failures.

**50.2.Q3** Does an upstream project have to accept the patch for this lesson to be complete?

**Expected reasoning:** No. A focused tested patch in an authorized maintained local fork, with rationale, reviewer response and handoff, can satisfy the task. Upstream acceptance must not be falsely claimed.

### Lab 50.2 review guidance
A successful contribution is narrow, tested and reviewable. The supplied reference code is new teaching code, not a mature upstream project and does not automatically satisfy this integration assignment. A local fork can meet the requirement, but it must genuinely have a maintained context and an independent review.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 50.3 — Portfolio, technical interviews and role-specific evidence

**50.3.Q1** What makes a portfolio case study more credible than a list of tools?

**Expected reasoning:** It shows a specific problem, personal contribution, constraints, correctness checks, reproducible results and limitations, with attribution and artifact links.

**50.3.Q2** How should the learner describe completing this program?

**Expected reasoning:** As completion of a self-study curriculum with specific demonstrated artifacts, not an accredited bachelor’s/master’s degree or institutional endorsement.

**50.3.Q3** Why can a well-explained negative result belong in a technical portfolio?

**Expected reasoning:** It can demonstrate rigorous evaluation, understanding of failure modes and sound deployment judgment, provided the baseline and evidence are trustworthy.

### Lab 50.3 review guidance
The strongest submissions align claims with available evidence and clearly distinguish self-study from accreditation. Reference answers may guide review but should not be read during the initial mock interview. An AI-only rehearsal is useful practice; record it as such rather than claiming independent human assessment.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

## Lesson 50.4 — Long-term learning, maintenance and final handoff

**50.4.Q1** Why should a trusted checksum manifest be retained separately from the archive it describes?

**Expected reasoning:** An attacker or accidental edit can change both files and the local manifest. A separately trusted record provides a comparison anchor; hashes still do not establish scientific correctness.

**50.4.Q2** What distinguishes a maintainer handoff test from an author-led demonstration?

**Expected reasoning:** The reviewer operates from the release documentation and exposes missing assumptions or setup. An author-led demonstration can conceal undocumented knowledge and manual fixes.

**50.4.Q3** What should the 90-day plan prioritize after Gate J?

**Expected reasoning:** One evidence-backed primary skill gap and one real reviewed contribution goal, with staged outcomes, sustainable effort and reassessment rather than many unrelated topics.

### Lab 50.4 review guidance
The final record must reference actual learner work and reviewer evidence. This package supplies templates and teaching examples, not a pre-signed completion certificate. Handoff succeeds when another person can use the artifact without the author’s machine. Open issues may remain if nonblocking, disclosed and owned; missing central reproduction is blocking.

**Do not infer completion:** check the submitted evidence against every mandatory condition in the original assignment.

# Transfer-problem solutions

These solutions correspond to the ten extra workbook problems, not the numbered lesson quizzes.

## 46-A — An ordering claim from a trace

**Problem:** A worker reports that a million relaxed all-atomic store-buffering runs never produced zero/zero. Write the strongest justified statement, the unjustified stronger statement, and one evidence source that could decide whether the outcome is allowed.

**Solution:** The experiment did not observe the outcome under the recorded conditions. It does not prove the outcome forbidden. A named language/ISA formal model and a valid execution argument or model checker can decide the relevant allowance; source and hardware layers must remain separate.

## 46-B — A cache experiment that changes two things

**Problem:** Compare a cache with 8 sets × 1 way × 64 bytes and one with 8 sets × 2 ways × 64 bytes. What changed? Construct a same-capacity associativity comparison, and state one limitation that survives the repair.

**Solution:** Capacity changes from 512 to 1,024 bytes as well as associativity. A 4-set × 2-way × 64-byte cache is a same-capacity comparison against the first. Index mapping and replacement behavior still differ, and a read-only serial model still excludes overlap, prefetching and real timing.

## 47-A — Repairing one kind of slack

**Problem:** Starting from setup slack +0.25 ns and hold slack −0.06 ns, add a buffer with +0.08 ns minimum delay and +0.12 ns maximum delay. Assume everything else unchanged. What are the new slacks?

**Solution:** Hold improves to +0.02 ns; setup worsens to +0.13 ns. The arithmetic is only a first estimate: route, slew, load and corner characterization may invalidate the assumed fixed increments.

## 47-B — Energy versus feasibility

**Problem:** Candidate P consumes 4 mW and processes 2 million items/s. Q consumes 3 mW and processes 1 million items/s. Which has lower energy per item? Which is feasible under a 3.5 mW hard power ceiling?

**Solution:** P uses 2 nJ/item and Q uses 3 nJ/item, so P is more energy-efficient. Only Q satisfies the 3.5 mW ceiling. A lower energy ratio does not override a hard peak or sustained power constraint.

## 48-A — A proof with no traffic

**Problem:** A queue harness assumes push is always false and proves that every popped value was previously pushed. Explain the vacuity risk and specify a cover or mutation that improves confidence.

**Solution:** The environment prevents meaningful enqueue traffic. Require a cover that accepts at least two distinct values and later pops them, inspect reachability, and mutate ordering or data storage so the intended property must fail. A cover does not replace the property proof; it exposes a too-restrictive environment.

## 48-B — Reset at the worst time

**Problem:** In the one-entry mailbox, the source has toggled request and is holding a payload. Only the destination is reset. Explain why treating this as an ordinary empty state is unsafe.

**Solution:** The request, acknowledgment and synchronizer histories can disagree about whether a payload belongs to the old or new epoch. The transfer could be dropped, duplicated or falsely acknowledged. The supplied model rejects unilateral reset; an implementation needs an explicit coordinated flush or an independently verified recovery protocol.

## 49-A — The wrong resampling unit

**Problem:** A study has twelve independently selected scenes, each producing 10,000 frame times for both configurations. Why is sampling all 120,000 frames as independent potentially misleading? Specify a defensible paired primary analysis.

**Solution:** Frames within a scene can be correlated and share scene difficulty. Treating them as independent can exaggerate precision. Define a scene-level metric first, pair the baseline and candidate within each scene, and resample independent scene pairs; repeated sessions may require a hierarchical model. The exact target population and sampling plan still matter.

## 49-B — A favorable metric switch

**Problem:** The approved primary metric is p95 frame time. After testing, the candidate improves the mean but worsens p95. Write an honest result sentence and one allowed next step.

**Solution:** The candidate improved mean frame time but regressed the prespecified p95 metric under the tested workload, so the primary hypothesis was not supported. Report both values and the failed cases. A follow-up hypothesis may study the mean or mechanism, but it must be labeled a new or exploratory analysis rather than silently replacing the original endpoint.

## 50-A — A clean-room mismatch

**Problem:** The independent reviewer reproduces the final table except one workload that is 15% slower. The thesis conclusion depends on that row. What should happen before Gate J closes?

**Solution:** Keep the gate open, compare environment, inputs, timing scope, stochastic variation and analysis scripts, and preserve both runs. Repair or narrow the claim, rerun the affected comparison and obtain reviewer confirmation. Do not average away a systematic discrepancy merely to meet a threshold.

## 50-B — The honest portfolio statement

**Problem:** Rewrite “I built a production GPU and earned a master’s degree” for a learner who implemented a queue accelerator, tested it in an educational flow and completed this self-study route.

**Solution:** Example: “Completed a master’s-level self-study specialization and built a queue accelerator evaluated with an educational RTL/physical-design flow. Implemented the stated logic, tests and analysis; no production silicon or accredited degree is claimed.” Specify actual personal contributions, tools, measured results and remaining limitations rather than copying unearned detail.
