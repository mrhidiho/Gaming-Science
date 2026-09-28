# Gate J
## Thesis, defense and maintainer handoff

**Package 11 · Volume 10 · Modules 49–50**

This guide turns the program’s final checkpoint into an executable review process. It is an assessment specification and a set of working methods, not a completed thesis, a promise of publication or a university credential. Use one primary project. Prior module work may supply components, baselines and tests, but cannot silently become evidence for a broader claim.

## 1. The minimum defensible contribution

A thesis-scale project needs a precise question, a justified method, implemented work, correctness evidence, a controlled evaluation and a clear statement of what the results establish. Novelty can be modest and carefully bounded. A replication with a useful extension, an explained failure regime or a rigorous negative result can be valuable. A large amount of code without a research question is not automatically a thesis.

Write the primary claim in one sentence. Identify its subject, intervention, comparison, workload population, outcome and conditions. Then write a sentence that would refute it. For example: “For a declared family of queue-dominated game-engine workloads, layout X reduces the selected latency metric relative to baseline Y without exceeding the fixed memory budget.” The refuting observation is a failure on the preregistered aggregate or required adverse cases, not a result on an unrelated benchmark.

A reviewed proposal is typically 3–5 pages and begins with 8–15 relevant sources. These are starting targets, not a quota that permits weak or redundant reading. Cite the closest work, the baseline, the method, known limitations and any specification used to establish legality or correctness. Distinguish what a source demonstrates from what you infer.

## 2. Choose one tractable route

### Route A — Architecture study

Investigate a bounded architectural choice for a game-related workload: cache geometry, request batching, queue depth, memory layout or a documented simulator configuration. A credible baseline, validated workload and explicit fidelity boundary matter more than simulating an entire console. Use at least three configurations where required by Module 46. Hold comparison scope constant and retain an adverse workload. A synthetic study can be legitimate when its generator and claim population are explicit; it is not automatically evidence about commercial games.

The minimum useful artifact is the workload generator or authorized trace, model or pinned simulator setup, a known-reference validation, results and sensitivity analysis. Possible extension: correlate one trend with a measured local workload without pretending the simple model predicts absolute frame times. Stop or narrow scope when trace provenance, simulator fidelity or execution-dependent behavior makes the intended claim unsupported.

### Route B — Verified queue or accelerator component

Implement a small component with a fixed interface, reset semantics and a precise performance or area question. Examples include a queue-management unit or a narrowly scoped data-layout transform. Compare a reference and candidate, prove useful properties, simulate accepted-data behavior and run an authorized educational physical flow if physical claims are central.

The artifact must distinguish logical correctness, cycle-level behavior and physical estimates. A netlist is not equivalent to placed-and-routed timing; a count invariant is not data-order proof; power estimates need an activity model. A project can conclude that the candidate is not worthwhile under the chosen constraint. Do not add a complete processor, operating system and game engine merely to make the project sound more ambitious.

### Route C — Reliability-aware engine/hardware interface

Study a bounded command-buffer, streaming or checkpoint protocol under explicit faults and reset conditions. The primary contribution might be a recovery policy, testability improvement or reduced cost under a stated failure model. Keep actual hardware access optional unless it is essential and authorized. A local controller model can support claims about its transitions, not about an IOMMU, analog reliability or undocumented hardware.

Specify accepted requests, ownership, completion rules, reset epochs and the allowed fault classes. Compare baseline behavior and the proposed change under the same injected campaign, with at least one adverse case. Treat prevention, detection, containment and recovery as different claims. Report uncorrectable cases and incomplete operations honestly.

## 3. Scope contract and exclusion list

Before implementing the candidate, agree with the reviewer on what is inside the thesis. Record the baseline revision, candidate mechanism, workloads, correctness oracle, primary metric, secondary metrics, uncertainty method, resource limits and intended result format. Exclusions should be concrete: “no branch prediction,” “read-only traces,” “single-clock FIFO,” or “coordinated reset only,” rather than the vague phrase “not production ready.”

Define stop conditions. A method that cannot be validated, a tool that cannot legally be obtained, a workload that cannot be released or a baseline that does not run can block the chosen route. A trigger should lead to a smaller fallback experiment while there is still time. Record the decision and whether it narrows the question. Do not conceal the fallback by rewriting the proposal after observing results.

## 4. Milestones and planning budget

The original volume estimate is 810–1,380 focused hours. The thesis’s 400–800 hours are a subset of that estimate, not an additional obligation. This allocation is an editable planning example:

| Milestone | Planning hours | Exit evidence |
|---|---:|---|
| Scope and literature | 40–80 | Reviewed question, source map, exclusions and refutation criterion. |
| Baseline and feasibility | 50–100 | Running baseline, correct small case, measurement protocol and risk triggers. |
| Candidate implementation | 120–230 | Versioned method, reference comparison, tests and reviewable decisions. |
| Controlled evaluation | 90–190 | Main comparison, adverse cases, ablation, sensitivity and raw data. |
| Report and artifact preparation | 70–140 | Traceable thesis argument, release candidate and reproduction instructions. |
| Defense and handoff | 30–60 | Independent result, defense record, closed revisions and maintainer acceptance. |

These six ranges sum to 400–800 hours. A project does not become better merely by using the high end. Reduce scope through review when a critical dependency slips. The learner should be able to show useful intermediate evidence rather than promising that the final week will resolve every risk.

## 5. Proposal review protocol

Send the reviewer the proposal, literature map and one-page experiment contract before the meeting. The reviewer should restate the hypothesis without help, identify its closest predecessor and name the observation that would weaken it. A mismatch in that restatement is a scope problem to repair now, not after implementation.

Review the baseline and feasibility evidence next. A downloaded repository is not a running baseline. Retain the exact revision, minimal invocation, expected output, actual output and correctness check. Estimate experiment duration using workload count × configurations × independent repetitions × run duration, then add setup and failure recovery. Reserve room for reruns rather than allocating the whole machine budget to a single pass.

Finish by assigning decisions, owners and due dates. Decisions may be approve, approve with repairs, narrow or change route. Approval is permission to proceed with the agreed experiment, not a promise that the hypothesis will succeed.

## 6. Experimental contract

Define the independent experimental unit before defining the confidence interval. A frame, scene, session, device and seed are not interchangeable units. If frames within a scene share conditions, treating every frame as an independent replication can create false precision. Pair baseline and candidate on the same independently selected units where the design supports it. Source S18 explains paired observations; the reference analysis routine demonstrates whole-pair resampling, not a universal statistical guarantee.

Specify exactly what the timer includes. A render phase, a whole frame, a cold start and an end-to-end interaction answer different questions. Record warmup, synchronization, clocks, power settings, thermal state and measurement overhead where relevant. Use a monotonic timer suitable for the actual platform. No package output constitutes a measurement of the user’s computer.

Choose one primary metric and document its aggregation. Means, tail percentiles, geometric speedup and throughput can move in different directions. State the percentile convention and the aggregation level. Keep raw samples so another reviewer can inspect the chosen reduction. Set correctness and resource feasibility as constraints rather than hoping a speedup outweighs corruption or an invalid operating condition.

Randomize or block run order where needed to reduce drift bias. Preserve seeds and input identities. Preregister exclusion rules and report all exclusions with reasons. If the tool crashes or the candidate times out, that can be a result, not a row to delete. Do not change the primary endpoint after observing an unfavorable value without declaring a deviation and separating exploratory analysis.

## 7. Baseline, ablation and sensitivity

The baseline is the actual reference configuration used for the primary comparison. Explain why it is credible and configure it competently. Disabling a baseline feature merely to make the candidate win is not a fair comparison unless the feature change is the question being studied.

An ablation removes or disables a claimed mechanism while keeping the remaining system as comparable as possible. It asks whether the mechanism contributes to the observed effect. A sensitivity study varies a parameter or assumption, such as queue depth, miss penalty, workload size or activity factor, and asks whether the conclusion survives. Renaming two configurations does not automatically produce either analysis.

Include an adverse case chosen before evaluation. A cache optimization may fail on streaming; a batching policy may harm tail latency; a physical optimization may fix setup while violating hold. Explain the failure mechanism with evidence. A thesis that clearly identifies where a method fails is stronger than a broad success claim obtained by hiding those cases.

## 8. Correctness before performance

Freeze an executable reference or a mathematical oracle for central behavior. Use boundary cases and metamorphic checks where a complete oracle is difficult. State the numerical equivalence contract: bitwise identity, bounded error, invariant preservation or another justified relation. Record compiler flags and transformations that affect the contract.

For hardware, keep a matrix of properties, assumptions, covers, configurations and outcomes. A completed proof applies to the given model and assumptions. A bounded check, simulation run or finite-state enumeration should be labeled as such. Check non-vacuity and retain at least one deliberate mutation with its failing trace or counterexample. A solver timeout is not a successful proof.

For a data-moving component, include reset, malformed inputs, accepted-transaction accounting and recovery. An epoch counter can reject stale modeled completions but cannot retroactively undo a real partial write. A digital CDC protocol can preserve logical order in a model without supplying an MTBF guarantee. Physical claims require actual tool reports and assumptions rather than the package’s synthetic PPA table.

## 9. Artifact release structure

Use a single release root with a human entry point and machine-readable inputs. The following layout is a recommendation, not a requirement to create empty files:

```text
thesis_release/
  README.md
  REPORT.pdf
  report_source/
  claims/claim_evidence.md
  environment/versions.json
  environment/licenses.md
  method/
  tests/
  data/raw/
  data/derived/
  experiments/manifest.json
  experiments/run_instructions.md
  results/central_table.csv
  results/failed_cases.md
  review/independent_reproduction.md
  review/defense_and_revisions.md
  handoff/maintainer_notes.md
  FILE_MANIFEST.json
```

Every central table row must be traceable to raw data or a clearly identified analytical derivation. Keep synthetic data separate from observed data. The release manifest provides integrity checks, not proof that results are true or authorship is original. Include required third-party notices and disclose proprietary inputs that cannot be distributed. Supply an authorized substitute fixture and explain what cannot be reproduced without restricted access.

Avoid instructions that silently download moving targets, require unknown credentials or execute destructive commands. Document a small smoke test before a long experiment. A reviewer should be able to estimate disk, memory and runtime before starting. Put generated outputs in a separate directory so the release’s reference files are not overwritten accidentally.

## 10. Claim-to-evidence audit

Select at least five major claims from the report. For each, identify its type, exact statement, supporting source or experiment, input/configuration, raw evidence, analysis step, output and limitation. A claim about correctness may need a proof or test contract, while a claim about performance needs a measurement contract. A literature claim needs the source and an accurate description of its scope.

Ask whether the evidence actually supports the quantifier. “On these twelve scenes” is narrower than “for all games.” “No error in this campaign” is narrower than “cannot fail.” “Routed in an educational flow” is narrower than “ready for manufacture.” The reviewer should be able to challenge one claim and watch the learner navigate directly to its evidence.

If an unsupported claim is not central, remove or narrow it. If it is central, the gate remains open until new evidence is obtained or the thesis is reframed around a defensible conclusion. Do not replace a missing result with a polished paragraph.

## 11. Thesis report outline

Start with an abstract that states the question, method, main result and principal limitation. The introduction motivates the problem without exaggerating its novelty. Related work locates the closest alternatives and the actual gap. The system and assumptions chapter defines the contract and exclusions. The method chapter explains the implemented change and why it might work.

The correctness chapter gives the oracle, tests, properties and known limits. The evaluation chapter states the protocol, presents the primary comparison, ablation and sensitivity, and retains failed cases. The discussion separates implications from speculation and treats validity threats directly. The conclusion states what was established and what remains unresolved. Appendices hold detailed derivations, configurations, larger tables and reproduction instructions.

The suggested 30–60 pages plus appendices is not a padding target. Compress repeated material and keep the central argument readable. A shorter rigorous report is preferable to a longer report that repeats background instead of presenting evidence. All borrowed diagrams, code, text and ideas need appropriate attribution and rights.

## 12. Independent reproduction runbook

The reviewer receives the frozen release, not the author’s already-configured workspace. Record reviewer identity or agreed attribution, date, machine/tool environment and whether the reviewer has previously seen the setup. The reviewer verifies integrity, reads the safety/resource notes and executes the smoke test without undocumented author intervention.

Next reproduce the central table or main result. Retain the command log, outputs and any manual changes. Compare against a prespecified tolerance appropriate to the method: deterministic model outputs may require exact agreement; physical measurements may require a justified statistical comparison. A vague statement that results “look similar” is not a reproduction criterion.

If execution fails, record the first failing command and observed behavior. The author may issue a new revision with a change log, but the reviewer must identify what changed and rerun the affected steps. A successful author rerun does not count as independent reproduction. An unresolved discrepancy that changes the conclusion is a gate blocker; a noncentral difference may narrow the claim with reviewer agreement.

## 13. Defense agenda

Hold a 30–45-minute review with a qualified reviewer or peer panel. A practical 40-minute allocation is five minutes for the question and contribution, eight for method, eight for evaluation and limitations, twelve for technical challenge, and seven for actions and decision. The panel may adjust this allocation while retaining substantive questioning.

The defense must include a derivation, a failed case and a live implementation question. “Live” can mean tracing relevant code, inspecting a property or rerunning a small experiment; it need not be a risky demonstration on a production system. Prepare a local fallback artifact for presentation failures, but distinguish that from the independent reproduction requirement.

### Technical challenge prompts

Explain why the chosen baseline is credible. Derive the metric or timing bound from its assumptions. Identify the smallest input that violates a naive implementation. Show a test that would catch an ordering mutation. Explain what your ablation removed and what it kept constant. Name a result that would refute your main claim. Show where a failed case appears in the release. Identify the strongest generalization your evidence does not support. Explain an assumption that could make a proof vacuous. Describe the maintainer’s first action after a regression. Attribute a borrowed component. Reproduce one central row from its raw source.

These are defense prompts, not additions to the sixty numbered lesson quiz questions. A fluent presentation without technical answers is not sufficient.

## 14. Gate J review rubric

| Category | Points | Evidence of strong work |
|---|---:|---|
| Question and relation to prior work | 10 | Falsifiable scope, accurate closest-work comparison and explicit exclusions. |
| Method and implementation | 25 | Substantive, understandable and versioned work with credible alternatives. |
| Correctness and verification | 20 | Appropriate oracle/properties, adverse cases, mutations and qualified guarantees. |
| Evaluation and interpretation | 20 | Fair baseline, declared metric, ablation, sensitivity and honest negative cases. |
| Reproducibility and traceability | 15 | Independent central result and a five-claim evidence audit. |
| Defense and handoff | 10 | Technical answers, closed revisions and a maintainer-ready release. |

The proposed package threshold is 80/100 with **all blocking conditions cleared**. This is a self-study review convention, not an accredited grade or a substitute for expert judgment. A lower score should produce specific repair actions rather than an unexplained rejection.

Blocking conditions are fabricated or misattributed evidence; a central correctness failure concealed or unresolved; absence of the required independent central reproduction; an evaluation that cannot support the stated claim; unsafe or unauthorized use central to the artifact; or inability to defend the core derivation and implementation. Negative performance results do not themselves block completion when the experiment and conclusion are rigorous.

## 15. Mature-codebase contribution and portfolio

Module 50 also asks for a maintainable integration. Use an existing mature project or a maintained local fork with a credible review process. Submit a narrow patch, tests that fail on the base where appropriate, the changed result, rationale and review responses. Upstream acceptance is not guaranteed and is not required to demonstrate that the learner can prepare and revise a maintainable contribution. The small teaching repository in this bundle is not itself evidence of mature-codebase integration.

Create three honest portfolio case studies from completed work across the curriculum; they need not be three new theses. For each, explain the problem, personal contribution, evidence, tradeoff and limitation. Complete three mock technical interviews addressing systems, algorithms and the selected specialization. Label the course as self-study. Never claim a degree, production hardware, external adoption or performance measurement that did not occur.

## 16. Maintainer handoff and closure

The maintainer needs more than a ZIP. Provide the system contract, supported environment, known failures, test commands, expected outputs, release procedure, dependency and rights record, recovery path and a prioritized issue list. Walk through one ordinary change and one failure-recovery scenario. Record where author-only knowledge was discovered and move it into documentation.

Close each review action with evidence and reviewer agreement. Freeze the final revision and archive the superseded one. Keep the final report, source, data, scripts, logs and review records consistent; a thesis PDF that refers to a different code revision is not a coherent release.

Finish with a single-priority 90-day learning plan. Choose the most important demonstrated gap, define a transfer task, reserve a review date and state observable success. Do not respond to every gap by starting another huge project. The final completion record should describe the actual artifacts and the scope of review, and should explicitly identify this as a self-study curriculum.
