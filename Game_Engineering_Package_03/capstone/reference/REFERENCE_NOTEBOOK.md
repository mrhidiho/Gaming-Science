# Reference notebook — evidence demonstration, not a student submission
## Scope and reproduction
This miniature reference illustrates the structure expected by Gate B. It is a supplied teaching artifact, not the learner's independent work or a completed external defense. Its code and CSV files cover chosen numerical cases; the full student problem set and reviewer challenge remain required.

Run `python capstone/reference/build_evidence.py --out outputs/reference_reproduction` from the extracted package root. The new directory contains model/synthetic numerical evidence, not physical measurements. Run `python run_benchmark.py --out outputs/new_benchmark --pairs 30` for new local timings. A previously existing output directory is rejected to prevent accidental overwriting.

## A specification and a proof
Let H be a finite list of finite health values and let C(k) count strictly positive values in H[0:k]. The loop invariant is that, before processing index k, count equals C(k), with 0<=k<=len(H). Initially k=0 and count=0, so the claim holds on the empty prefix. Processing H[k] increments count exactly when that entry is positive, hence establishes C(k+1). At exit k=len(H), so count equals the number of living entries. The nonnegative integer len(H)-k decreases once per step, proving termination under ordinary sequential execution. The implementation still needs tests for strict positivity and prefix bounds.

A universal requirement can say: for every living entity e, there exists an owner o in the owner registry whose ID equals e.owner_id. Its negation is a living entity for which no such owner exists. It is not equivalent to requiring one single owner for all entities. An empty live-entity set makes the universal claim true without proving that any entity exists.

For induction, let S(n)=1+...+n. The n=0 base gives zero. Assuming S(k)=k(k+1)/2, adding k+1 gives (k+1)(k+2)/2, establishing the next case. Thus S(100)=5050. This proof uses exact integers and does not prove every floating-point summation implementation.

## Geometry
In geometry.json, units are chosen as meters, transformations act on column vectors, rotations are right-handed and y is up. Parent T(10,0,0)*Rz(pi/2) maps the child offset (2,0,0) to (10,2,0). The child origin has homogeneous w=1; a direction has w=0 and does not receive the translation. A scalar-first quarter-turn quaternion rotates +x to +y. The zero-normalization case rejects the request rather than inventing a direction. The inverse round-trip tolerance is a numerical comparison, not symbolic equality.

## Numerical dynamics
The constant-acceleration oracle follows by integrating v'=a, then x'=v. For the oscillator x'=v, v'=-100*x, the chosen initial state (1,0) yields x(t)=cos(10t), v(t)=-10*sin(10t) and energy 50 in model units. The explicit Euler map adds h*v to x and subtracts 100*h*x from v using the old state. Expanding the next-step energy gives E_next=(1+100*h^2)*E, so any positive step amplifies energy in this particular undamped model.

spring_trajectories.csv compares explicit and semi-implicit methods at the same final time T=2. The h=0.25 case lies beyond omega*h<2 for the semi-implicit linear oscillator and is intentionally adverse. spring_summary.csv reports errors against the analytic path and energy. A stable-looking semi-implicit trajectory can still have phase error; bounded energy is not exact conservation or exact position.

The derivative experiment uses exp(x) at x=1 and centered differences. A moderate perturbation can outperform an extremely small one because roundoff competes with truncation error. An unresolvable perturbation is labeled instead of interpreted as a perfect derivative. Quadrature is checked against integral_0^1 x^2 dx=1/3. Trapezoid results need not be exact for curved functions.

## Probability and sampling evidence
The illustrative detector with p=0.01, sensitivity=0.9 and false-positive rate=0.05 has posterior 0.009/(0.009+0.0495)=2/13. The high sensitivity alone is not the posterior. For rewards 0,5,20 with probabilities .70,.25,.05, E=2.25 and Var=26.25-2.25^2=21.1875. loot_counts.csv records seeded numerical trials, not observed player behavior. Matching expected frequencies approximately is a finite-sample check, not proof of the model's applicability.

sampling.csv includes 900 Hz and 100 Hz signals at fs=1000. For integer n, cos(2*pi*(fs-f)*n/fs)=cos(2*pi*n-2*pi*f*n/fs)=cos(2*pi*f*n/fs). The corresponding sine acquires a negative sign. This is why an alias magnitude without phase information is insufficient to reconstruct a waveform. filters.json contrasts phase-dependent raw checker decimation with averaging and records full convolution. The simple short prefilter is an illustration, not a certified anti-alias design for arbitrary signals.

## Optimization
For f=(x-3)^2, the fixed-step error satisfies e_next=(1-2*alpha)*e. The numerical sweep records alpha=.25,.5,1,1.1. Only an achieved gradient tolerance permits converged=true. The two-variable case f=(x-3)^2+3*(y+1)^2 has Hessian eigenvalues 2 and 6; a fixed step must respect the most restrictive direction, so alpha=.4 can be unstable even though a scalar example with smaller curvature tolerates it. The sample logs do not claim a convergence theorem for arbitrary nonconvex objectives.

## A real measured experiment and its limits
The separate measured_benchmark directory contains actual elapsed-time observations from Python 3.13.5 on Linux in the authoring environment. These are not synthetic timing targets. Each workload compares identical queries and validates hit counts with an independent arithmetic oracle. Method B includes construction of the set; excluding that cost would answer a different question. Raw observations and metadata preserve randomized paired order and the test conditions.

For the recorded size=4096, one-query workload, the median for linear-list membership is about 0.0464 ms and the set-build-plus-query median is about 0.3550 ms. With 32 queries at that size, the corresponding medians are about 1.1596 ms and 0.3642 ms. These are particular noisy observations, not universal speed ratios. They illustrate why amortizing setup across more queries can change the comparison. Use the actual raw CSV and recorded precision for any reproduction rather than these rounded narrative values.

The supplied paired intervals are conditional on the stated inference model; consecutive runs on shared infrastructure may violate independence or normality. Medians, means and tail percentiles answer different questions, and a tiny sample can conceal a rare pause. The experiment does not establish native C++ performance, GPU behavior, player experience or a causal law about all hardware.

## What an independent reviewer must still do
A reviewer should rerun the artifact, inspect proofs and test the changed-coordinate, timestep and misleading-average questions. Automated tests cover bounded code examples and do not replace that review. The learner must write the extended notebook and own tests, log external problem work, and identify reference-derived sections honestly.
