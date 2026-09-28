
# Game Systems Reference
## Conventions before formulas

A formula is safe to use only when its variables, units and coordinate convention match the implementation. This reference summarizes the conventions used by the teaching kernels. Your engine may choose different conventions, but it must adapt at boundaries rather than mixing them silently. It is not a replacement for the derivations in the lessons.

## Simulation contract

| Item | Teaching convention | Boundary test |
|---|---|---|
| Length/time | Meters and seconds | Known speed over a known duration |
| Fixed step | h explicitly recorded | Equal input tape with different render rates |
| Collision normal | A toward B | Swap bodies and reverse the normal |
| Contact geometry | Closed-set touching in circle/grid kernel | Exact tangency and cell boundary |
| Tick state | S_t is before applying I_t | Correction at tick zero |
| Entity identity | Stable ID plus generation/epoch when reused | Despawn/reuse and delayed message |
| Transform | State row/column convention explicitly | Non-identity parent and mesh transform |
| Audio frame | One time instant across all channels | Interleaved buffer length = frames*channels |
| Authority | Server applies validated intentions | Claimed final position not trusted |
| Evidence | Scope tied to build/platform/method | Reproduce from a clean folder |

## Collision and dynamics

Unordered pairs for n bodies: n(n-1)/2. A conservative broad phase produces a candidate superset of true contacts; candidate equality with brute force is not required. For a grid cell size c, use floor(x/c), especially for negative coordinates. Insert full shape bounds, then deduplicate canonical pairs.

Circles overlap under the closed-set convention when |p_B-p_A| <= r_A+r_B. For coincident centers, normalizing displacement is undefined; use a documented deterministic fallback. AABB separation can be checked axis by axis. Geometric tolerance, contact skin, solver slop and replay comparison tolerance are separate policies.

In 2D, scalar cross(a,b) = a_x*b_y - a_y*b_x. Angular velocity crossed with an offset r is (-omega*r_y, omega*r_x). Contact-point velocity is v + omega cross r. Relative normal speed is v_n = dot(v_B_contact-v_A_contact, n); negative means approaching under the A-to-B convention.

For a frictionless contact, K = w_A + w_B + invI_A*(r_A cross n)^2 + invI_B*(r_B cross n)^2, where w is inverse mass. For approaching bodies and K>0, J = -(1+e)*v_n/K. Apply -J*n to A and +J*n to B, including their angular effects. Units: inverse mass is kg^-1, inertia is kg*m^2 and impulse is N*s. A static body uses zero inverse mass/inertia, not an arbitrarily huge finite mass.

Momentum is conserved in an isolated two-body impulse test. Elastic restitution e=1 preserves kinetic energy in the ideal frictionless model; e<1 dissipates normal relative motion. Gravity, damping, constraints and correction can change what should be conserved in a full scene. An invariant must match the experiment.

Semi-implicit Euler: v_(k+1) = v_k + a_k*h, x_(k+1) = x_k + v_(k+1)*h. Constant acceleration over time T=N*h gives a position error relative to the analytic solution of 0.5*a*T*h for this update ordering. With a=-10, T=1 and h=1/60, the error is about -0.083333 m. Halving h halves that particular error; this does not establish the convergence order of a complete collision simulation.

For a one-axis swept point, compute the interval of t for which lo <= x+v*t <= hi, intersect with [0,dt], and explicitly handle v=0 and initial overlap. For a finite-radius circle/sphere approximation, inflate obstacle bounds by the radius. A full rotating convex-shape continuous solver needs more than this slab kernel. [S01, S02]

## Constraint budgets

Measure constraint residual independently from runtime. A distance residual is |length(p_B-p_A)-rest_length|; a useful scene summary is the maximum across constraints. Report iteration count, substeps, timestep, warm starting and ordering. Iterating the same step and reducing timestep are not interchangeable operations. Positional projection can reduce distance error while changing energy; do not call it an energy-conserving solver.

Cap solver work and the number of continuous impacts processed per step. Test the cap being exhausted. A limit without a fallback can convert a difficult scene into an infinite loop or unbounded frame. [S02, S19]

## Transforms, skinning and IK

With column vectors, a local-to-parent matrix L and parent-to-world matrix P compose as W=P*L. Descendant transforms follow the parent chain. Skinning uses current joint global transforms and inverse bind transforms, with any mesh-node correction required by the asset convention. At bind pose, the effective skin transform should reproduce the source geometry. Test a non-identity mesh transform, not only identity scenes. [S03, S04]

For two planar links l1,l2 and target distance d, cos(elbow)=(d^2-l1^2-l2^2)/(2*l1*l2). Clamp numerical roundoff into [-1,1], distinguish unreachable targets from roundoff, and select an elbow branch. shoulder=atan2(y,x)-atan2(l2*sin(elbow),l1+l2*cos(elbow)). Reachable radial range is |l1-l2| to l1+l2. At zero distance, direction needs a policy; a formula alone does not choose a stable pose.

Quaternions q and -q encode the same rotation. For short-path interpolation, account for their dot-product sign and normalize where the method requires it. Blending animation does not decide gameplay authority or release action-owned resources.

## Audio and event timing

A callback receiving F frames at sample rate f_s has nominal block duration F/f_s seconds. With 256 frames and 48 kHz, this is 5.333 ms. Interleaved stereo contains 512 scalar samples for that block. Actual scheduling/headroom is a platform matter; a nominal duration is not a guaranteed uninterrupted CPU window. Avoid allocation, blocking I/O and unbounded work in the real-time path. [S05, S06]

For a sine oscillator, phase advances by 2*pi*f/f_s per frame and must persist between blocks. A sufficient peak bound for a sum of unit-amplitude waves is sum(abs(gain_i)) <= 1. It is conservative and does not describe perceived loudness. The C++ sample instead uses a prebuilt wavetable and eight gains capped at 0.125 each.

Equal-power pan: theta=(pan+1)*pi/4, gains=(cos(theta),sin(theta)). The sum of squared gains is one. Independent category controls still need a final mix/headroom policy.

One-shot identity: (match_epoch,tick,entity_id,event_index). Retain already presented identities outside restored simulation state for the supported replay window. Expire old history deliberately, define new-epoch handling and distinguish presentation deduplication from persistent reward idempotency. Critical information needs a tested alternative channel, not just a decorative icon. [S23]

## AI decision contracts

A* prioritizes f(n)=g(n)+h(n). With unit-cost four-neighbor grids, Manhattan distance is an admissible, consistent heuristic. Agent radius/clearance belongs in the navigation representation; steering/collision still execute movement. Found, unreachable and budget_exhausted are different statuses. A stale asynchronous result must not overwrite a newer navigation generation. [S08]

A utility selector chooses among valid scores and may retain the current action unless another exceeds it by a defined margin. Specify ties, invalid scores and cancellation. A behavior tree uses explicit statuses and node lifecycle; neither representation by itself guarantees correct cleanup. [S09]

Alpha-beta pruning preserves minimax value under its game/evaluation assumptions while changing the explored node set. Under a strict budget, return a move from the last complete iteration or a legal prevalidated fallback. Distinguish node budgets from wall-clock budgets and record move ordering. [S10]

Logistic classifier: z=w dot x+b, p=sigmoid(z), cross-entropy gradient dL/dw=(p-y)*x and dL/db=p-y. Use a stable sigmoid implementation. Split independent episodes/scenarios before preprocessing/model selection; select using validation, freeze, then evaluate held-out test data. Include a rules baseline, error analysis, inference cost and a tested runtime fallback. [S11]

## Networking and persistence

A sequence acknowledgement in the supplied protocol is contiguous: every input through that number has been applied. A newer snapshot restores authority; the client discards acknowledged inputs and replays the remaining ordered inputs exactly once. Reconciliation changes simulation state; render smoothing must not quietly become authority. [S12]

Interpolation at render time t between snapshots (t0,x0),(t1,x1) uses alpha=(t-t0)/(t1-t0), then x=(1-alpha)*x0+alpha*x1, only when a valid bracket exists. Arrival times and simulation timestamps are not the same. Missing delta baselines need a full-state recovery. Relevance filtering must happen before transmission to limit hidden-state exposure. [S13]

For rollback, restore S_t before applying corrected I_t, then replay through the last executed tick. Memory is snapshot_bytes*retained_ticks plus input/event metadata. A 2 MB snapshot retained for 120 ticks is roughly 240 MB before overhead. Determinism is an explicit engine/environment contract, not a benefit automatically obtained by saving a seed. [S14, S24]

Idempotent operation IDs require payload consistency. Exact retries reuse the committed result; same ID/different payload is a conflict. Atomically record both the operation and reward mutation in one transaction. A response lost after commit does not mean the operation failed. Authentication, authorization and idempotency solve distinct problems. [S15, S16]

## Performance and release

Frame interval for target rate f is 1000/f milliseconds. At 60 Hz, approximately 16.667 ms. A mean below budget does not prevent stalls. For sorted N samples, nearest-rank percentile p uses index ceil(p*N)-1. Record this convention, sample count, repeated runs, raw distributions and timing boundaries.

Amdahl bound: if fraction p of original time is accelerated by factor s, overall speedup is 1/((1-p)+p/s). It assumes the rest of the measured workload stays unchanged and ignores additional overhead unless incorporated. Use it to reject impossible claims before coding.

Pseudo-localization expands visible strings while preserving placeholders; it does not establish a correct translation, all language shaping, or broad accessibility. Remapped controls and prompts need one shared binding source. Human task observation is distinct from automated property checks. [S07, S25, S26]

Validate resource sizes before allocation and enforce actual byte limits while reading. A hash is an integrity comparison, not publisher authentication. Stage updates separately from the active release and switch only after validation. Replacing a file atomically under documented filesystem conditions is not equivalent to guaranteed power-loss durability on every platform. [S17, S18]

## Debugging questions across subsystem boundaries

What owns this state? In which units and coordinate space is it expressed? Which tick/version produced it? May a different thread or asynchronous callback still read it? Can the work or memory grow without a cap? Which inputs are trusted? What happens when a message, device or file is missing? What exact experiment supports the claim? What first-failure record would distinguish the plausible causes?

Answer these questions before adding a new abstraction or optimizing away evidence. A readable boundary contract often prevents more defects than a sophisticated subsystem algorithm.

# Reference Directory

S-prefixed entries are the focused primary-source companions consulted for this expansion, September 28, 2026. Numbers are stable identifiers; gaps are intentional. R-prefixed entries preserve the original program reading directory. External books, papers, documentation and library source are not bundled; the explanations, exercises and demonstration code in this package are original teaching material. Pin installed versions in your own evidence rather than treating a mutable documentation page as an installed build.

## S01: Collision documentation

Box2D project. Shape queries, broad phase, dynamic tree and time-of-impact limitations.

[Open primary source](https://box2d.org/documentation/md_collision.html)

## S02: Simulation documentation

Box2D project. Stepping, contacts, solver settings and the documented determinism contract.

[Open primary source](https://box2d.org/documentation/md_simulation.html)

## S03: glTF tutorial: Skins

Khronos Group. Joint transforms, inverse bind matrices and mesh-node correction.

[Open primary source](https://github.khronos.org/glTF-Tutorials/gltfTutorial/gltfTutorial_020_Skins.html)

## S04: glTF 2.0 specification

Khronos Group. Normative asset, animation and skinning data contracts.

[Open primary source](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)

## S05: Writing a callback function

PortAudio project. Callback constraints and real-time-safe execution discipline.

[Open primary source](https://portaudio.com/docs/v19-doxydocs/writing_a_callback.html)

## S06: SDL_AudioStreamCallback

SDL project. SDL3 audio stream callback contract; consult the API for the chosen integration.

[Open primary source](https://wiki.libsdl.org/SDL3/SDL_AudioStreamCallback)

## S07: Xbox Accessibility Guidelines

Microsoft. Game accessibility design/testing guidance, not a legal-compliance certification.

[Open primary source](https://learn.microsoft.com/en-us/xbox/accessibility/guidelines)

## S08: CS188: Informed search

University of California, Berkeley. A*, heuristics and search guarantees under stated assumptions.

[Open primary source](https://inst.eecs.berkeley.edu/~cs188/textbook/search/informed.html)

## S09: Introduction

BehaviorTree.CPP project. Behavior-tree concepts, statuses and implementation context.

[Open primary source](https://www.behaviortree.dev/docs/intro/)

## S10: CS188: Minimax

University of California, Berkeley. Adversarial search and alpha-beta reasoning.

[Open primary source](https://inst.eecs.berkeley.edu/~cs188/textbook/games/minimax.html)

## S11: Automatic differentiation with torch.autograd

PyTorch project. Gradient/parameter concepts; framework use is optional for the core synthetic exercise.

[Open primary source](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)

## S12: Networked movement in the Character Movement Component

Epic Games. A maintained engine comparison for authority, prediction and correction.

[Open primary source](https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-networked-movement-in-the-character-movement-component-for-unreal-engine)

## S13: Snapshot Interpolation

Glenn Fiedler. Author’s technical explanation of interpolation, jitter and visual delay.

[Open primary source](https://gafferongames.com/post/snapshot_interpolation/)

## S14: GGPO SDK repository

GGPO authors. Primary implementation/documentation for rollback networking concepts.

[Open primary source](https://github.com/pond3r/ggpo)

## S15: Transaction documentation

SQLite project. Transaction boundaries and behavior.

[Open primary source](https://www.sqlite.org/lang_transaction.html)

## S16: Atomic Commit in SQLite

SQLite project. Atomicity assumptions and storage failure considerations.

[Open primary source](https://www.sqlite.org/atomiccommit.html)

## S17: os.replace documentation

Python Software Foundation. Replacement semantics and platform/filesystem conditions.

[Open primary source](https://docs.python.org/3/library/os.html#os.replace)

## S18: zipfile documentation

Python Software Foundation. Archive processing and extraction boundaries.

[Open primary source](https://docs.python.org/3/library/zipfile.html)

## S19: Fix Your Timestep!

Glenn Fiedler. Simulation/render time separation and work-budget hazards.

[Open primary source](https://gafferongames.com/post/fix_your_timestep/)

## S23: XAG 103: Additional channels for audio and visual cues

Microsoft. Critical information through more than one channel.

[Open primary source](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103)

## S24: Deterministic Lockstep

Glenn Fiedler. Input synchronization and deterministic simulation requirements.

[Open primary source](https://gafferongames.com/post/deterministic_lockstep/)

## S25: XAG 107: Input

Microsoft. Input/remapping accessibility considerations.

[Open primary source](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107)

## S26: XAG 101: Text display

Microsoft. Readable interface text and testing considerations.

[Open primary source](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/101)

## Original program reading IDs

These inherited assignments remain part of the full study route. S entries above focus the expanded lesson tasks; they do not replace all external study.

**R17: RFC 9293: Transmission Control Protocol** — IETF / RFC Editor. Transport semantics; reference reading after networking foundations. [Assigned source](https://www.rfc-editor.org/rfc/rfc9293.html)

**R19: 15-462/662 Computer Graphics** — Carnegie Mellon University. Rendering, geometry and animation course structure and exercises. [Assigned source](https://15462.courses.cs.cmu.edu/fall2021/)

**R20: 15-466/666 Computer Game Programming** — Carnegie Mellon University. Runtime systems and game-production programming. [Assigned source](https://graphics.cs.cmu.edu/courses/15-466/)

**R22: SDL3 documentation** — SDL project. Windowing, input, audio and platform services; do not mix SDL2 and SDL3 examples. [Assigned source](https://wiki.libsdl.org/SDL3/FrontPage)

**R23: Physically Based Rendering, fourth edition** — Matt Pharr, Wenzel Jakob, Greg Humphreys. Rendering mathematics and implementation; use chapter titles in lesson assignments. [Assigned source](https://www.pbr-book.org/4ed/contents)

**R26: Programming with C++ in Unreal Engine** — Epic Games. Engine comparison after C++ foundations, not a beginner substitute. [Assigned source](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)

**R28: Box2D documentation** — Box2D project. Collision, constraints and simulation reference. [Assigned source](https://box2d.org/documentation/)

**R29: Xbox Accessibility Guidelines** — Microsoft. Accessibility design and testing; not a legal-compliance certificate. [Assigned source](https://learn.microsoft.com/en-us/xbox/accessibility/guidelines)

**R45: AddressSanitizer documentation** — LLVM Project. Memory-error instrumentation, limitations and supported toolchains. [Assigned source](https://clang.llvm.org/docs/AddressSanitizer.html)

**R46: CS188 Introduction to Artificial Intelligence textbook** — University of California, Berkeley. Search, games, decision processes, learning and probabilistic reasoning. [Assigned source](https://inst.eecs.berkeley.edu/~cs188/textbook/)

**R47: Dive into Deep Learning** — Aston Zhang, Zachary Lipton, Mu Li and Alexander Smola. Learning fundamentals, gradients, generalization and reproducible exercises; pin compatible framework versions. [Assigned source](https://d2l.ai/)

