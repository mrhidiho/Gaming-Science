<!-- Package 10, Volume 9; September 28, 2026 -->

# Use the key after an independent attempt

This key contains the 60 original quiz answers, solutions to the 40 additional graduate problems, entry-diagnostic guidance and lab review criteria. It does not contain completed learner research submissions. A matching final number without the assumptions, reasoning and units is not full understanding.

For quizzes, correct misconceptions and then answer a fresh variant. For graduate problems, distinguish a valid derivation from an empirical observation. For labs, use the reference to locate the first disagreement rather than copying its implementation and claiming independent work. Independent reviewer signatures and learner measurements are never prefilled.

# Entry diagnostic: answers and repair

### D1

Solve [[2,-1],[-1,2]] x = [1,1], and state why this matrix is SPD.

**Answer:** x=[1,1]. Its eigenvalues are 1 and 3, both positive, and it is symmetric. Equivalent principal-minor or quadratic-form reasoning is acceptable. Repair: Modules 07 and 41.2 / R07.

### D2

For E(x)=0.5*k*(x-rest)^2, give the force and its units when k is N/m.

**Answer:** F=-k*(x-rest), in newtons when displacement is meters. Repair: calculus/physics in Volumes 2 and 6 / R41.

### D3

Under independent finite-variance sampling, what increase in sample count halves standard error?

**Answer:** Four times as many samples. State the assumptions; correlated history reuse need not follow this rule. Repair: Module 09 / R09.

### D4

Give the work and span of a balanced binary reduction on 1,024 values.

**Answer:** 1,023 pairwise combinations and 10 levels under the binary-tree model. Memory and synchronization add implementation costs. Repair: Module 14 and Lesson 42.1.

### D5

At an assumed sustained 1 GB/s using decimal units, what lower-bound transfer time corresponds to 10 MB, ignoring setup?

**Answer:** 0.01 s = 10 ms. This is a bandwidth model, not a measured transfer, and it excludes setup and contention. Repair: Modules 16 and 38 / R43.

### D6

Why can parallel floating-point sums differ from a serial sum?

**Answer:** Regrouping changes intermediate rounding; floating-point addition is not exactly associative. Decide on bitwise or error-bounded correctness. Repair: numerical representation and Module 37.

### D7

Why is a callback capturing a destroyed owner unsafe, and name one valid lifetime strategy.

**Answer:** The callback may access invalid memory. Examples include retained ownership with a correct lifetime, or generation/weak-handle validation at dispatch with a safe cancellation protocol. Repair: Modules 11 and 18 / R11.

### D8

Can an area density and a solid-angle density be added directly in an MIS denominator?

**Answer:** No. Convert to a common measure with the correct geometry Jacobian before combining densities. Repair: Modules 21-23 / R23.

### D9

Why can a global GPU spin barrier that requires all workgroups be deadlock-prone?

**Answer:** Resident groups can occupy resources while waiting for groups that cannot be scheduled. Use API-supported synchronization/dispatch boundaries. Repair: Modules 18 and 37 / R37.

### D10

Does a fixed random seed and a source repository alone guarantee another reader can reproduce a table?

**Answer:** No. Inputs, configurations, dependencies, exact commands, timing boundaries and analysis may still be missing; other nondeterminism may matter. Repair: Module 20 and Lesson 41.4.

# Module 41 answer guidance

Graduate numerical methods and research practice

## Lesson 41.1 — Reading research as claims, assumptions and evidence

### Original quiz answers

**Q1. Why distinguish equal-error from equal-sample comparisons?**

They control different quantities and can support different performance conclusions.

**Q2. What makes a claim-evidence table useful?**

It connects each conclusion to its actual mathematical or experimental support and exposes unsupported generalization.

**Q3. Does a failed reproduction immediately disprove a paper?**

No. Configuration, implementation, data, numerical and interpretation differences must first be investigated.

### Graduate problem solutions

**P1. An abstract says "4x faster" but the figure measures samples per second, excluding preprocessing. Write a narrower claim and one required end-to-end experiment.**

P1. Claim only 4x higher sampling throughput in the reported configuration. Run total preparation plus sample generation plus reconstruction on identical inputs at the same quality threshold; report amortization across reuse counts.

**P2. Your reproduction misses the reported value by 15%. Design a diagnostic order that separates estimator, scene, precision, parameter and timing-boundary differences.**

P2. First verify scalar identities and independent-reference agreement. Then match scene/data and parameters, inspect precision and randomization, and audit the timer boundary. Change one factor at a time, retaining both successful and unsuccessful runs. A discrepancy remains unresolved until those controls justify a narrower explanation.

### Lab review checkpoint

The selected publication and version are unambiguous. The planned result can be evaluated without inventing unavailable hardware measurements.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 41.2 — Conditioning, sparse systems and iterative solvers

### Original quiz answers

**Q1. What is the 2-norm condition number of diag(1,10^-6)?**

10^6.

**Q2. Why can a small residual coexist with substantial solution error?**

An ill-conditioned system can amplify small equation perturbations into large changes in the solution.

**Q3. What matrix property is required by standard conjugate gradient?**

A symmetric positive-definite matrix, or the corresponding Hermitian positive-definite complex case.

### Graduate problem solutions

**P1. For A=diag(1,10^-6), compute relative residual and relative forward error for b=(1,10^-6), x=(1,0).**

P1. ||r||/||b||=10^-6/sqrt(1+10^-12), approximately 10^-6. ||e||/||x*||=1/sqrt(2), approximately 0.7071. The loose upper bound kappa times relative residual is approximately 1.

**P2. Why might a preconditioner that halves iteration count still lose overall time? Give a break-even formula.**

P2. Let setup cost be S, original iterations k, original iteration cost c and extra preconditioner application cost m. It wins only if S+(k/2)(c+m)<kc. For one solve, expensive setup can dominate; for repeated right-hand sides, state how setup is amortized.

### Lab review checkpoint

Known-solution error meets the declared tolerance. Preconditioner setup and application costs are retained.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 41.3 — Constrained optimization, derivatives and optimality conditions

### Original quiz answers

**Q1. What is the constrained minimizer in the example?**

x=y=0.5, with objective 0.5 and multiplier -1 under the stated Lagrangian sign convention.

**Q2. Does zero gradient prove a general nonconvex point is a minimum?**

No. It may also be a saddle or maximum.

**Q3. Why vary finite-difference step size in a derivative check?**

Large steps incur truncation error while extremely small steps amplify floating-point roundoff.

### Graduate problem solutions

**P1. Project t=(1,2,4) onto sum(x)=1. Is the result also a projection onto the probability simplex?**

P1. lambda=(7-1)/3=2; x=(-1,0,2). It satisfies the affine constraint but is not in the probability simplex because one component is negative. Nonnegativity requires an additional constrained projection.

**P2. Derive the two columns of the two-link arm Jacobian and identify a singular pose for unit links.**

P2. Column one is (-l1 sin(t1)-l2 sin(t1+t2), l1 cos(t1)+l2 cos(t1+t2)); column two is (-l2 sin(t1+t2),l2 cos(t1+t2)). At t2=0 the columns are parallel, so rank is at most one and the local inverse is singular.

### Lab review checkpoint

The Lagrangian sign convention is recorded. The full lab extends beyond the provided closed-form projection.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 41.4 — Experimental design, uncertainty and reproducible graduate work

### Original quiz answers

**Q1. Why identify the statistical unit?**

It determines what observations can reasonably be treated as independent for the intended inference.

**Q2. What does an ablation test?**

Whether removing or changing a component changes the outcome in a way that supports its claimed contribution.

**Q3. Why reserve held-out workloads?**

They test whether tuning improvements generalize beyond the cases used to choose parameters.

### Graduate problem solutions

**P1. One scene produces 10000 frames and another produces 100. How could a frame-weighted mean distort a claim about typical scenes?**

P1. The first scene receives 100 times the weight, even if the intended population treats scenes equally. Summarize within scene and use a justified scene-level aggregation, or explicitly define the workload-weighted estimand.

**P2. Why is the fixed-ratio bootstrap unit test not evidence that the experimental method is statistically sound?**

P2. The unit test checks arithmetic and reproducibility for known inputs. It does not test independence, representative sampling, exclusion rules, tuning leakage, interval coverage under the actual design or the adequacy of the sample size.

### Lab review checkpoint

The independent unit is justified rather than inferred from row count. A reviewer can regenerate the analysis from raw data.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

# Module 42 answer guidance

Advanced parallel and GPU algorithms

## Lesson 42.1 — Parallel reductions, scans and work-span analysis

### Original quiz answers

**Q1. How many levels are in a balanced binary reduction of 1,024 values?**

10.

**Q2. How many pairwise combines does that reduction require?**

1,023.

**Q3. Why can parallel floating-point sums differ from serial sums?**

Changing grouping changes rounding because floating-point addition is not exactly associative.

### Graduate problem solutions

**P1. Derive the output length of compaction from flags and exclusive offsets without a second full sum.**

P1. For n>0, length=offset[n-1]+flag[n-1]. For n=0 it is zero. Each kept position has a distinct count of earlier kept positions, proving unique writes and stability.

**P2. Give floating-point values for which regrouping changes the result, then explain why this does not invalidate an exact-integer scan test.**

P2. Under a typical floating format, (10^20+(-10^20))+3 can yield 3 while 10^20+((-10^20)+3) can yield 0. The rounded algebra differs from exact integers or modulo arithmetic. A correct test must use the contract of the implementation being tested.

### Lab review checkpoint

Empty and partial groups behave correctly. GPU completion is marked pending until device execution is actually verified.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 42.2 — Tiling, data reuse and asynchronous pipelines

### Original quiz answers

**Q1. Why can larger tiles hurt performance?**

They can increase resource usage, reduce residency or cause spills and boundary overhead.

**Q2. What ownership rule is essential for double buffering?**

A buffer must not be consumed before preparation completes or overwritten before its current consumer finishes.

**Q3. Why retain a non-asynchronous baseline?**

It provides a simpler correctness and portability reference for evaluating the extra pipeline complexity.

### Graduate problem solutions

**P1. Under the stated 4-byte ideal stage model, compute intensity and double-buffer storage for B=16 and B=64.**

P1. B=16 gives 4 operations/input-byte and 16B^2=4096 bytes of double-buffered input storage. B=64 gives 16 operations/input-byte and 65536 bytes. These are model counts, not feasibility or occupancy guarantees.

**P2. Four tiles take copy=6 and compute=2 units. Derive ideal serial and two-buffer pipelined completion times.**

P2. Serial time is 4*(6+2)=32. Copy is the bottleneck, so the ideal pipeline is 4*6+2=26, including the final compute drain. Required ownership and engine independence must hold.

### Lab review checkpoint

The numerical output matches the declared tolerance. The fallback path remains tested.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 42.3 — Irregular workloads, wavefront scheduling and load balance

### Original quiz answers

**Q1. Why can average task cost hide poor completion time?**

A few long tasks can dominate the final tail after most workers become idle.

**Q2. Why avoid a global spin barrier requiring every group to be resident?**

Unschedulable groups may never run while resident groups wait, causing deadlock.

**Q3. Is sorting tasks always beneficial?**

No. Sorting cost, added latency and data movement can exceed coherence gains.

### Graduate problem solutions

**P1. Show why an empty queue while one job is executing is insufficient evidence of termination.**

P1. The executing job can later publish another job. Terminating at the empty snapshot discards valid work. A correct protocol must include in-flight work and establish that no future producer remains.

**P2. A reordering stage costs 0.8 ms and saves 0.5 ms of traversal. When could it still be justified, and what would need measurement?**

P2. It loses 0.3 ms under the stated one-frame timing boundary. It could be justified by another measured benefit, such as lower tail latency or reuse across multiple queries, but that changes the claim and requires a complete accounting of costs and quality.

### Lab review checkpoint

Every accepted job is completed or explicitly canceled, never lost or duplicated. No model-only timing is presented as a device result.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 42.4 — Portable performance and integration-quality evaluation

### Original quiz answers

**Q1. Does portable performance require one fixed launch configuration?**

No. Valid specialization or bounded tuning may be necessary across targets.

**Q2. What should be said when only one GPU was tested?**

The evidence is limited to that tested configuration; broader portability remains unverified.

**Q3. Why measure integration cost?**

A standalone kernel gain may not survive real data preparation, scheduling and result consumption.

### Graduate problem solutions

**P1. If f=0.05, what is the largest possible application speedup even with an infinitely fast kernel and no overhead?**

P1. The limit is 1/(1-0.05)=1.05263x. Eliminating only 5% of runtime cannot justify a claimed 2x application improvement under the same workload.

**P2. Distinguish unsupported from untested in a device capability matrix and explain why that distinction matters.**

P2. Unsupported means a known required capability is absent or deliberately excluded; untested means evidence has not been collected. The latter cannot justify either a success claim or a categorical assertion of incompatibility.

### Lab review checkpoint

The fallback passes the same functional tests. No unavailable GPU result is filled with a CPU timing.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

# Module 43 answer guidance

Advanced rendering and reconstruction

## Lesson 43.1 — Monte Carlo light transport and multiple importance sampling

### Original quiz answers

**Q1. What is the balance weight for strategy 1 in the example?**

0.25 under equal sample counts.

**Q2. Why is p(x)>0 on relevant support important?**

Otherwise nonzero contributions can never be sampled and the estimator can be biased or undefined.

**Q3. What sample-count increase ideally halves standard error for independent finite-variance samples?**

Approximately four times as many samples.

### Graduate problem solutions

**P1. Convert p_area=0.25 per square meter at distance 2 m and light cosine 0.5 to a solid-angle density.**

P1. p_omega=0.25*4/0.5=2 per steradian. If the light was selected with probability 1/K, multiply the complete directional density by 1/K.

**P2. A path survives roulette with probability 0.25 and has pre-roulette contribution 3. What contribution should a surviving path carry, and what is the expectation?**

P2. A surviving path contributes 3/0.25=12; terminated paths contribute zero. The expectation is 0.25*12=3. This calculation concerns roulette only, not separate depth or clamping bias.

### Lab review checkpoint

The chosen densities cover all relevant nonzero contributions. A finite-depth image is not labeled an unbiased full-transport solution.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 43.2 — Real-time ray tracing, dynamic acceleration and hybrid pipelines

### Original quiz answers

**Q1. Why can a cheap BVH refit become a poor long-term choice?**

Large motion can degrade bounds and increase traversal cost.

**Q2. Is saving 1 ms of tracing worth 4 ms of per-frame rebuild cost?**

Not under that stated per-frame workload; total time increases by 3 ms.

**Q3. Why compare animated scenes?**

Dynamic updates and temporal behavior can dominate costs or artifacts absent in a static scene.

### Graduate problem solutions

**P1. Derive the break-even reuse count for two policies with build costs bA,bB and query costs qA,qB when qB<qA.**

P1. B wins when bB+F*qB<bA+F*qA, so F>(bB-bA)/(qA-qB). Handle nonpositive numerators separately; these assumptions exclude changing query cost during reuse.

**P2. Why can an animated test invalidate a conclusion obtained from a single screenshot?**

P2. Motion changes hierarchy quality, update frequency, correspondence, resource hazards and temporal image quality. A still frame observes none of those sequence-dependent costs and failures.

### Lab review checkpoint

Accelerated and brute-force hits agree within the selected numerical tolerance. Hardware-only claims require hardware evidence.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 43.3 — Spatiotemporal reuse, reservoirs and denoising

### Original quiz answers

**Q1. Why cannot reused samples always be treated as new independent samples?**

Reuse can introduce correlation and change the estimator's sampling structure.

**Q2. Why is same-pixel history not enough to establish correspondence?**

Different surfaces can occupy that pixel after motion or disocclusion.

**Q3. What should be compared in a denoised rendering benchmark?**

Quality, bias/artifacts, temporal behavior and total runtime, not only the raw ray count.

### Graduate problem solutions

**P1. For fixed candidates with weights (1,2,7), show the first item's final selection probability using the sequential replacement rule.**

P1. The first item starts selected. It survives candidate 2 with probability 1/3 and candidate 3 with probability 3/10, so final probability is (1/3)*(3/10)=1/10.

**P2. Why is W/(M*p_hat(Y)) necessary in the simple candidate-resampling estimator, rather than outputting only f(Y)?**

P2. Y follows the weighted resampling distribution, not the original integration measure. Conditional expectation with the normalization becomes the ordinary candidate importance average. Omitting it generally integrates under the selection distribution and changes the target quantity.

### Lab review checkpoint

The selected sample probability is distinguished from the final estimator weight. A complete ReSTIR claim is not made from the primitive alone.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 43.4 — Differentiable and neural rendering under engineering constraints

### Original quiz answers

**Q1. Does automatic differentiation guarantee the desired gradient estimator?**

No. The modeled computation, discontinuities and stochastic estimator must still match the intended objective.

**Q2. Why hold out entire scenes for some rendering evaluations?**

It tests generalization beyond correlated frames or content seen during training.

**Q3. When should training cost be included?**

When the claimed practical benefit depends on total preparation, deployment or repeated use, not only one isolated inference.

### Graduate problem solutions

**P1. Derive the albedo least-squares optimum and explain what happens when all basis values are zero.**

P1. Set derivative sum_i b_i(rho*b_i-y_i)=0, obtaining rho=sum(b_i*y_i)/sum(b_i^2); project to [0,1] for the box-constrained scalar problem. A zero denominator means the data do not identify rho.

**P2. A method needs 600 seconds of preparation and saves 2 milliseconds per frame. How many frames are required to break even on time alone?**

P2. 600/0.002=300000 frames, ignoring all other changes. At 60 frames/s that is 5000 seconds of playback, about 83.3 minutes. State whether the prepared artifact is reused across sessions and whether quality is equivalent.

### Lab review checkpoint

The optimized objective matches the claimed physical or statistical quantity. The supplied scalar oracle is not mistaken for a trained network or full inverse renderer.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

# Module 44 answer guidance

Advanced engine systems and simulation research

## Lesson 44.1 — Large-world scheduling, streaming and critical-path control

### Original quiz answers

**Q1. Why can a camera teleport defeat ordinary prefetching?**

It changes the needed content abruptly, bypassing assumptions about gradual motion.

**Q2. Why is origin rebasing an interface issue?**

Physics, rendering, networking and stored references must agree on coordinate changes.

**Q3. What distinguishes a bounded degradation policy?**

It limits work and resource use while explicitly choosing which quality or availability guarantees may temporarily relax.

### Graduate problem solutions

**P1. What is the ideal critical path of A=2, B=3 after A, C=4 after A and D=1 after B and C? Can four workers reduce it?**

P1. 7 ms through A,C,D. Four workers do not shorten these dependencies; improving the algorithm or overlap is required.

**P2. A resident budget is 100 MB, existing assets use 70 MB and a new 20 MB asset needs 25 MB of overlapping scratch/staging. Does a final-residency-only check safely admit it?**

P2. Final residency would be 90 MB, but overlapping memory is 115 MB if charged to the same physical budget. Admission must reserve transient bytes or defer/evict safely. Separate budgets still require a combined physical-memory feasibility check.

### Lab review checkpoint

Resident memory and transient overlap are separately bounded. Coordinate conventions are explicit at physics/render/network boundaries.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 44.2 — Deformable simulation, variational models and solver tradeoffs

### Original quiz answers

**Q1. What force follows from the example spring energy?**

-k*(x-rest).

**Q2. Does numerical stability guarantee physical accuracy?**

No. A stable trajectory can still have large discretization error or use an unsuitable physical model.

**Q3. Why vary timestep and solver iterations independently?**

They affect different sources of error and can reveal hidden parameter dependence.

### Graduate problem solutions

**P1. Compute the first and second scalar updates for w=1, C=1 initially, alpha=0.01 and h=0.1 with accumulated multipliers.**

P1. alpha_tilde=1, delta_lambda=-0.5, x=0.5 and lambda=-0.5. The second numerator is -0.5-1*(-0.5)=0, so no further update occurs.

**P2. If a timestep is halved while physical compliance is held fixed, how does alpha_tilde change? Does this alone prove that trajectories at the two timesteps match?**

P2. alpha_tilde increases by a factor of four. This preserves the intended compliance scaling in the formulation but does not eliminate time-discretization, collision, nonlinear or finite-iteration differences. Compare at equal physical time and convergence criteria.

### Lab review checkpoint

Compliance scales with h squared as specified by the selected formulation. A paper reproduction is distinguished from a scalar teaching oracle.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 44.3 — Distributed game state, consistency and overload behavior

### Original quiz answers

**Q1. Why is duplicate authority dangerous?**

Two participants may both commit effects that should occur only once under one owner.

**Q2. What is a retry storm?**

Many failed or slow requests trigger additional retries that worsen overload.

**Q3. Can a small local demo establish internet-scale reliability?**

No. It supports only the tested model and scale unless broader evidence is provided.

### Graduate problem solutions

**P1. Why is a lease on the sending server insufficient to reject a delayed stale write at an external sink?**

P1. The sink may receive an old request after authority has moved; the old sender may also be paused or partitioned. A monotonic epoch checked by the sink, with correctly coordinated ownership and persistence assumptions, prevents that stale operation from committing.

**P2. A request can be retried three times after its original attempt. What is the maximum attempt amplification for one logical request, and why is that not a sufficient overload policy alone?**

P2. Four attempts per logical request. Many simultaneous clients can still exceed capacity; deadlines, admission limits, bounded outstanding requests and controlled retry timing are also needed.

### Lab review checkpoint

Stale authority is rejected where the irreversible effect commits. Durability, scale and network claims do not exceed the tested model.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 44.4 — Formal specifications, replay and reliability-oriented engine design

### Original quiz answers

**Q1. How do safety and liveness differ?**

Safety excludes forbidden events; liveness requires eventual progress under stated assumptions.

**Q2. Why must liveness assumptions mention scheduling or worker progress?**

An environment that never lets work run can prevent completion regardless of the local algorithm.

**Q3. Does proving an abstract model automatically prove all implementation code?**

No. The relationship between the model and implementation must be established and checked.

### Graduate problem solutions

**P1. Does exhaustive safety exploration of the supplied one-request model establish eventual completion? Explain.**

P1. No. Eventual completion is a liveness property; the model may permit infinite stuttering or starvation. It requires explicit progress assumptions and a separate liveness check or argument. Exhaustiveness is relative to the finite safety model.

**P2. Why should an artifact keep event/state data as well as their hashes?**

P2. A hash locates disagreement but does not explain it. Event and state data allow inspection of the first differing input, schedule or field and make replay failures actionable.

### Lab review checkpoint

The deliberate bug is detected, preventing a vacuous passing result. Replay records enough nondeterminism for the claimed execution model.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

# Module 45 answer guidance

Compilers, shader languages and engine specialization

## Lesson 45.1 — Intermediate representations, SSA and dataflow analysis

### Original quiz answers

**Q1. What does SSA require of each value?**

One defining assignment in the representation.

**Q2. Why is the example phi node not always constant 1?**

The else predecessor supplies 2 unless that path is proven unreachable.

**Q3. What is the role of a fixed point in dataflow analysis?**

It marks a state where further propagation under the analysis rules no longer changes the computed facts.

### Graduate problem solutions

**P1. For USE[B]={a}, DEF[B]={b}, OUT[B]={b,c}, compute IN[B].**

P1. IN[B]={a} union ({b,c} minus {b})={a,c}.

**P2. Two loop phis swap x and y on a backedge. Why must their incoming values be selected simultaneously?**

P2. Both phis must read the predecessor values. Sequentially updating x before reading it for y can duplicate a value instead of swapping, violating the edge semantics.

### Lab review checkpoint

Phi values are selected by the actual predecessor and assigned simultaneously. No full compiler-verification claim is made from a bounded interpreter.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 45.2 — Alias analysis, vectorization and legal optimization

### Original quiz answers

**Q1. Why is alias analysis important for reordering loads and stores?**

Two apparently different references may access the same storage, creating dependencies.

**Q2. Are iterations of a[i]=a[i-1]+1 independent?**

No. Each depends on the previous result.

**Q3. Why record floating-point compiler options?**

They can permit transformations that change rounding, exceptional-value handling or other required semantics.

### Graduate problem solutions

**P1. Do the half-open logical ranges [0,8) and [8,16) overlap? What about [0,8) and [7,9)?**

P1. The first pair does not overlap because the shared endpoint is excluded from the first range. The second pair overlaps on [7,8). Zero-length ranges overlap nothing.

**P2. Why does a passing randomized test suite not by itself prove an optimization legal for every input?**

P2. It samples a finite subset and may miss rare values, aliases or control-flow paths. A semantic argument states why all accepted inputs preserve behavior; tests check that the implementation follows that argument.

### Lab review checkpoint

Numerical equivalence is required before speed is considered. Sanitizer timings are not mixed with release performance measurements.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 45.3 — Domain-specific languages, specialization and safe JIT execution

### Original quiz answers

**Q1. How many combinations do four independent binary options create?**

16.

**Q2. Why limit the effects allowed in a DSL?**

Restrictions make validation, optimization and safe execution more tractable.

**Q3. Why keep an interpreter alongside compiled execution?**

It provides a portable fallback and a simpler reference for semantic testing.

### Graduate problem solutions

**P1. How many combinations result from eight independent binary options, and what happens after adding two more?**

P1. 2^8=256. Ten options produce 1024, a fourfold increase. Runtime frequencies and resource limits should guide which variants are materialized.

**P2. Why can a cache key based only on source text be incorrect after a compiler or target change?**

P2. Identical source can compile under different semantics, ABIs or target capabilities. The cached result may be incompatible or wrong unless those inputs and relevant tool versions are part of its identity.

### Lab review checkpoint

Invalid trees and oversized inputs fail before execution. Restricted interpretation is not described as an operating-system sandbox.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

## Lesson 45.4 — Compiler/hardware co-design and graduate artifact review

### Original quiz answers

**Q1. Why can a faster instruction fail to improve the application?**

Packing, spills, data movement or unaccelerated work can outweigh the arithmetic savings.

**Q2. What distinguishes reproduction from extension?**

Reproduction recreates an existing result; extension changes or adds a clearly identified method, setting or analysis.

**Q3. Is publication acceptance mandatory for Gate I?**

No. The requirement is rigorous, reproducible work and an independent technical review.

### Graduate problem solutions

**P1. Compute the application speedup in the worked example and explain why the 2x kernel number is insufficient.**

P1. 12/12.2 is about 0.984, a slowdown of roughly 1.7% in elapsed time. Packing and spill/transfer overhead outweigh the arithmetic savings. The timing boundary determines what the 2x number supports.

**P2. A reviewer can run the code but cannot regenerate the main table because scene files are missing. Has Gate I passed?**

P2. No. Executable code alone is insufficient for the central reproducibility requirement. Supply authorized inputs or an adequately scoped replacement experiment, rerun it and narrow the claim as necessary.

### Lab review checkpoint

Reproduction and extension are separately named. The compiler requirement and any pending device validation remain visible.

The full procedure and remaining acceptance checks are in the workbook. Review the derivation and an adverse case in addition to inspecting output. A bundled reference result does not supply the learner's own experiment or independent review.

