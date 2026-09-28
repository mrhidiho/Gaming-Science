# Answer Key

Attempt the lesson quiz and the changed-input exercise before consulting this key. Each of the five lesson questions uses 0-2 formative points: incorrect/missing, partially reasoned, or correct with the required conditions/calculation. The expanded lesson score is out of 10. A target of 8/10 does not waive a core misconception, lab, assigned study or engine-transfer requirement. Module reviews are additional checks.

# Module 26: Collision detection and physical simulation

## Lesson 26.1: Broad phase, narrow phase and geometric robustness

### Question 1

**Prompt:** May a correct broad phase return false positives?

**Answer guidance:** Yes. Narrow-phase tests can reject them; false negatives are the dangerous case.

### Question 2

**Prompt:** How many unordered pairs exist for 100 objects?

**Answer guidance:** 4,950.

### Question 3

**Prompt:** Why document contact-normal orientation?

**Answer guidance:** Impulse and separation calculations depend on a consistent direction between the two bodies.

### Question 4

**Prompt:** With 250 bodies, how many exhaustive unordered pairs are possible? What relationship must hold between true-contact and candidate sets?

**Answer guidance:** 250 x 249 / 2 = 31,125. Every true-contact pair must occur in the candidate set; the reverse inclusion is unnecessary. Extra candidates are a cost, not a correctness defect.

### Question 5

**Prompt:** A circle spans four cells but its center occupies one. Is center-only insertion sufficient? Give a repair and a duplicate-pair policy.

**Answer guidance:** No. A neighbor can intersect the circle outside its center cell. Insert its complete bounding box into every intersected cell, emit canonical body-ID pairs, and deduplicate before applying impulses.

**Repair task:** Port the broad-phase ownership and pair-order contract into the Volume 5 engine. Keep the brute-force oracle in a debug/headless target, independent of the grid implementation. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 26.2: Rigid bodies, angular motion and collision impulses

### Question 1

**Prompt:** What velocity change follows from 6 N*s applied to 2 kg?

**Answer guidance:** 3 m/s in the impulse direction.

### Question 2

**Prompt:** Why can an off-center impulse cause rotation?

**Answer guidance:** It changes angular momentum through the lever arm relative to the center of mass.

### Question 3

**Prompt:** Why use zero inverse mass for a static body?

**Answer guidance:** It naturally produces no velocity change under impulse calculations without relying on infinite numerical values.

### Question 4

**Prompt:** Two 2 kg bodies have velocities 3 and 0 m/s and restitution 0.5. Compute impulse, final velocities and total final kinetic energy.

**Answer guidance:** With n from A to B, relative speed is -3, effective inverse mass is 1, and j = 4.5 N*s. A ends at 0.75 m/s; B at 2.25 m/s. Final kinetic energy is 0.5*2*(0.75^2+2.25^2) = 5.625 J. Momentum remains 6 kg*m/s.

### Question 5

**Prompt:** A 6 N*s horizontal impulse acts 0.5 m above the center of a body with inertia 0.25 kg*m^2. What angular-velocity change results?

**Answer guidance:** Using r=(0,0.5) and J=(6,0), cross(r,J)=-3 kg*m^2/s, so delta omega=-3/0.25=-12 rad/s. Reversing the stated axis convention changes the represented sign, not the physical motion.

**Repair task:** Implement separate force and impulse commands in your engine. Add tests proving that the renderer cannot directly overwrite the physics-owned transform of a dynamic body. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 26.3: Constraints, iterative solvers and continuous collision detection

### Question 1

**Prompt:** How far does 30 m/s travel in 1/60 second?

**Answer guidance:** 0.5 m.

### Question 2

**Prompt:** Why can increasing solver iterations help?

**Answer guidance:** It can reduce residual constraint error, though cost rises and other modeling problems can remain.

### Question 3

**Prompt:** Does CCD remove every numerical simulation problem?

**Answer guidance:** No. It addresses certain between-step collision failures under its motion and solver assumptions.

### Question 4

**Prompt:** A point starts at 0 m and moves at 30 m/s toward the slab [0.24,0.26] m during a 1/60 s tick. What is the entry time, and why does an endpoint test miss it?

**Answer guidance:** Entry is 0.24/30 = 0.008 s. The final point is at 0.5 m, beyond the slab, so neither endpoint overlaps even though the motion crosses it.

### Question 5

**Prompt:** A chain becomes less stretchy when solver iterations increase. Does this prove conservation of energy or solve projectile tunneling?

**Answer guidance:** Neither. It shows reduced constraint residual in that experiment. Energy must be measured under the chosen correction model; endpoint collision detection can still miss a between-step crossing.

**Repair task:** Add a debug CCD flag, a per-tick impact cap and residual telemetry to your engine. Demonstrate that a dense contact scene cannot make one tick loop without a bound. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 26.4: Physics testing, determinism and engine integration

### Question 1

**Prompt:** Is same-machine repeatability proof of cross-platform determinism?

**Answer guidance:** No. Compiler, arithmetic and implementation differences can still matter.

### Question 2

**Prompt:** Why identify the first divergent tick?

**Answer guidance:** It localizes the origin of disagreement before later effects amplify it.

### Question 3

**Prompt:** What should happen when a simulation first creates a NaN?

**Answer guidance:** Capture a useful diagnostic and reject or isolate invalid state according to policy rather than letting it propagate silently.

### Question 4

**Prompt:** Using semi-implicit Euler with acceleration -10 m/s^2, zero initial velocity, t=1 s and h=1/60 s, what is the position error against the analytic solution?

**Answer guidance:** The error is 0.5*a*t*h = -5/60 = -0.083333... m. The numerical position is about -5.083333 m rather than -5 m. Halving h halves this error in this constant-acceleration setup.

### Question 5

**Prompt:** Two replay hashes agree, but an omitted AI cooldown differs. What has been proved, and what must change?

**Answer guidance:** Only the serialized subset agreed. Include every future-affecting authoritative field, including cooldowns and random state; use explicit schema ordering, then compare the next transition after restore as well as the current snapshot.

**Repair task:** Publish a versioned engine state schema and first-divergence replay report. Classify the result as same-environment repeatability unless other named platform combinations were actually tested. Reattempt with one changed input or boundary condition and explain why the result differs.

## Module 26 review answers

### Review 1

**Prompt:** A projectile is missed only near cell boundaries. Which intermediate artifacts distinguish a broad-phase defect from a narrow-phase defect?

**Answer guidance:** Capture full shape bounds, covered cells, canonical candidate pairs, filtering decisions and final contacts at the same tick. If the true pair is absent from candidates, inspect membership/filtering; if present but rejected, inspect geometry/tolerance policy. Use an independent oracle.

### Review 2

**Prompt:** Why can an off-center contact require a smaller impulse than a center-only calculation for the same initial normal speed?

**Answer guidance:** The contact-point effective inverse mass includes rotational response. A positive rotational term increases K, reducing J for the same restitution target. The impulse changes both translation and rotation; comparing only center speed is incomplete.

### Review 3

**Prompt:** An engineer doubles solver iterations and calls it equivalent to halving the timestep. Explain the error.

**Answer guidance:** Iterations reduce algebraic constraint error within a step; a smaller timestep changes integration, collision sampling and force accumulation. They can interact but are not equivalent. Compare separate tables for iteration count and timestep.

### Review 4

**Prompt:** What extra evidence is needed beyond matching two final-state hashes?

**Answer guidance:** Per-tick canonical states/hashes, a defined complete state schema, seeded inputs, exact environment/build, deliberate divergence detection, physical invariants and analytic checks. A match says little about physical accuracy or an untested platform.

### Review 5

**Prompt:** Your simple engine and a maintained library disagree on bounce height. What should be controlled before deciding either is wrong?

**Answer guidance:** Units, shapes/skins, timestep/substeps, gravity, integration method, restitution threshold, contact offset, solver iterations, damping, sleep settings and library version. State known approximations and compare an isolated analytic case first.

# Module 27: Animation, audio and interactive timing

## Lesson 27.1: Skeletons, transforms and skinning

### Question 1

**Prompt:** Why evaluate parent transforms before dependent children?

**Answer guidance:** A child world transform depends on the parent world transform.

### Question 2

**Prompt:** What should ordinary normalized skinning weights sum to?

**Answer guidance:** One.

### Question 3

**Prompt:** Why avoid directly interpolating arbitrary rotation-matrix entries?

**Answer guidance:** The result may cease to be a valid pure rotation and can introduce scale or shear.

### Question 4

**Prompt:** A root rotates 90 degrees and its child has local translation (1,0). Where is the child in world coordinates under column-vector parent*local composition?

**Answer guidance:** At (0,1), assuming the root is at the world origin. The parent rotation acts on the child translation; adding the unrotated translation would mix spaces.

### Question 5

**Prompt:** Why should G_j * inverse(B_j) be identity in the bind pose, and what extra transform is needed for a mesh-local output buffer?

**Answer guidance:** At bind pose G_j equals B_j, so their product cancels. For mesh-local output, prepend inverse(mesh_world) when G_j and B_j are defined consistently in world space; the exact convention must match the imported asset.

**Repair task:** Add an immutable skeleton resource and a per-instance pose buffer to the existing engine. Demonstrate two actors sharing one skeleton without sharing playback state. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 27.2: Animation blending, state machines and inverse kinematics

### Question 1

**Prompt:** Can every IK target be reached?

**Answer guidance:** No. Geometry, joint limits and constraints can make targets unreachable.

### Question 2

**Prompt:** What is the maximum reach of two collinear links of length 1 each?

**Answer guidance:** 2 units.

### Question 3

**Prompt:** Why define root-motion ownership?

**Answer guidance:** Animation and physical simulation otherwise may apply incompatible displacement to the same object.

### Question 4

**Prompt:** For links of length 1 and 1 and target (1,1), compute one elbow and shoulder solution. Verify it with forward kinematics.

**Answer guidance:** One branch has theta2=pi/2 and theta1=0. The endpoint is (cos(0)+cos(pi/2), sin(0)+sin(pi/2))=(1,1). The other elbow branch is also possible under an appropriate shoulder angle.

### Question 5

**Prompt:** An action clip moves the root 0.3 m while the physics controller also moves it 0.3 m in the same tick. What contract is missing?

**Answer guidance:** Root-motion authority. Animation should either supply a displacement for collision-resolved movement or remain visual while physics supplies movement; adding both gives an unintended 0.6 m step.

**Repair task:** Implement the state/pose separation in your engine and make the animation trace visible in the inspector. Add one cancellation test that frees an action-owned resource. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 27.3: Digital audio, mixing and real-time callback discipline

### Question 1

**Prompt:** What duration does 256 frames represent at 48 kHz?

**Answer guidance:** Approximately 5.33 ms.

### Question 2

**Prompt:** Why avoid disk reads inside an audio callback?

**Answer guidance:** Their unpredictable blocking time can exceed the audio deadline.

### Question 3

**Prompt:** Does halving the buffer automatically improve every aspect of audio?

**Answer guidance:** No. It can reduce buffering latency while increasing deadline pressure and underrun risk.

### Question 4

**Prompt:** How many sample values are in 256 stereo frames, and what duration do they represent at 48 kHz?

**Answer guidance:** There are 512 sample values, but the duration is 256/48000 seconds, about 5.333 ms. Channel count changes storage, not the number of time instants.

### Question 5

**Prompt:** Why can draining a lock-free command queue until empty still violate a callback deadline? Give a bounded alternative.

**Answer guidance:** A producer can keep adding work, and each command may have a nontrivial cost. Limit commands per callback, cap voices and output frames, and define overflow/coalescing behavior. Lock-free does not mean bounded total callback work.

**Repair task:** Connect the native mixer pattern to your engine audio adapter. Keep device-specific code outside the simulation and demonstrate graceful operation when no output device exists. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 27.4: Spatial audio, animation events and multimodal accessibility

### Question 1

**Prompt:** Is stereo panning a complete spatial-hearing model?

**Answer guidance:** No. It represents only some directional cues.

### Question 2

**Prompt:** Why give presentation events stable identities during replay?

**Answer guidance:** To recognize previously presented events and apply a deliberate deduplication policy.

### Question 3

**Prompt:** Why provide a non-audio equivalent for a critical cue?

**Answer guidance:** The player may not hear the cue because of disability, environment or settings.

### Question 4

**Prompt:** At center pan under the equal-power rule, what are the left and right gains? What quantity is preserved?

**Answer guidance:** Both gains are sqrt(0.5), approximately 0.7071. Their squares sum to one. This is a mathematical gain property, not a guarantee of equal perceived loudness for every playback setup.

### Question 5

**Prompt:** A rollback snapshot restores the set of already-played sounds to an earlier version. What bug follows, and where should this set live?

**Answer guidance:** Previously presented sounds can play again during resimulation. Presentation deduplication should live outside rollback state, keyed by stable event identity and bounded by the replay horizon, with a new epoch for a new match.

**Repair task:** Route your engine events into interchangeable audio, visual and optional haptic adapters. Demonstrate one critical task with audio muted and no dependence on color alone. Reattempt with one changed input or boundary condition and explain why the result differs.

## Module 27 review answers

### Review 1

**Prompt:** A bind-pose mesh moves when skinning is enabled. Give a structured diagnosis.

**Answer guidance:** Check joint index order, current global transforms versus bind globals, inverse bind matrices, mesh-node correction and multiplication convention. Test one fully weighted vertex with a non-identity mesh transform; do not patch with an unexplained inverse.

### Review 2

**Prompt:** An action is canceled during a blend but its attack sound still fires. What ownership rules are missing?

**Answer guidance:** Separate gameplay action authority from visual blending; define event emission/cancellation and whether a marker still belongs to a valid action. Use stable event IDs and trace the action generation. Blending a pose does not authorize gameplay effects.

### Review 3

**Prompt:** A callback has a lock-free queue but misses deadlines. Give three plausible reasons.

**Answer guidance:** Unbounded draining, allocation/loading or expensive DSP, too many voices/large block work, and operating-system scheduling can all matter. Cap work, preallocate and measure the actual device path; lock-free is not a hard real-time guarantee.

### Review 4

**Prompt:** Why should the presentation-event deduplication ledger not be restored with the rolled-back simulation state?

**Answer guidance:** Restoring it would forget already presented events and replay audible/visible one-shots. Keep bounded presentation history separate, while restoring the authoritative event-generation state needed for deterministic resimulation.

### Review 5

**Prompt:** What makes a critical visual audio alternative successful rather than merely present?

**Answer guidance:** A tester can identify the required state and complete the task without sound. The cue must be readable, timely, distinguishable without color alone where relevant, and not obscured or dependent on an inaccessible control.

# Module 28: Game AI, decision systems and machine learning

## Lesson 28.1: Navigation graphs, steering and dynamic obstacles

### Question 1

**Prompt:** How do pathfinding and steering differ?

**Answer guidance:** Pathfinding selects a route; steering produces local movement to follow or adjust that route.

### Question 2

**Prompt:** Can the example 1.0-wide agent pass through the 0.8-wide doorway?

**Answer guidance:** Not under the stated no-overlap model.

### Question 3

**Prompt:** Why bound replanning work?

**Answer guidance:** Large or frequent searches can consume the frame budget and harm responsiveness.

### Question 4

**Prompt:** For a four-connected unit-cost grid, what is the Manhattan heuristic from (0,0) to (3,2)? Does a two-expansion budget prove a route is impossible?

**Answer guidance:** The heuristic is 5. Exhausting two expansions only proves the configured budget was consumed; return budget_exhausted unless the frontier was actually exhausted without a path.

### Question 5

**Prompt:** A smoothed path segment cuts across an obstacle corner although every original grid node is free. What validation is missing?

**Answer guidance:** Clearance along the continuous segment for the full agent footprint. Validate swept movement or use a smoothing method constrained by navigable geometry; point-node validity alone is insufficient.

**Repair task:** Add a globally budgeted navigation queue and stale-result rejection to the engine. Demonstrate a wide and a narrow actor receiving different valid routes. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 28.2: Behavior trees, utility systems and explainable decisions

### Question 1

**Prompt:** What statuses should a multi-frame action expose?

**Answer guidance:** At least a defined running/progress state, success, failure and cancellation behavior.

### Question 2

**Prompt:** Why can nearly tied utility scores cause oscillation?

**Answer guidance:** Small input changes repeatedly reverse the preferred action.

### Question 3

**Prompt:** Why is a decision trace valuable?

**Answer guidance:** It makes selection criteria and failures visible for testing, tuning and designer review.

### Question 4

**Prompt:** The current action scores 0.60, the best alternative scores 0.64 and the switching margin is 0.05. Which action remains, assuming both are valid?

**Answer guidance:** The current action remains because 0.64 is not greater than 0.65. If the current action becomes invalid, validity overrides the hysteresis rule.

### Question 5

**Prompt:** A canceled navigation action receives its asynchronous result later and starts moving again. What state or ownership check should prevent this?

**Answer guidance:** Associate requests with an action/entity generation or cancellation token. The completion path verifies the action is still active and owns that request before installing the path; cleanup must release resources exactly once.

**Repair task:** Expose a bounded decision trace in the engine inspector, including facts, scores, chosen action, cancellation reason and outstanding request generation. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 28.3: Adversarial search, planning and simulation budgets

### Question 1

**Prompt:** Does alpha-beta change the minimax objective when applied correctly?

**Answer guidance:** No. It prunes branches that cannot affect the same result under the search assumptions.

### Question 2

**Prompt:** How many depth-6 paths arise from branching factor 10 without pruning?

**Answer guidance:** About 10^6, or one million.

### Question 3

**Prompt:** Why use a fallback action?

**Answer guidance:** The decision deadline may arrive before the planned search completes.

### Question 4

**Prompt:** A root maximizer has already found value 3. A new minimizing child first reveals leaf value 2. Why may its remaining leaves be pruned?

**Answer guidance:** The minimizing child can finish at 2 or lower, so it cannot improve on the root alternative worth 3. Under the stated deterministic minimax model, the branch cannot change the chosen value.

### Question 5

**Prompt:** Depth 3 completed but depth 4 exhausts its node budget halfway through the root. Which result should iterative deepening return, and what should be reported?

**Answer guidance:** Return the last fully completed depth-3 result, or a legal fallback if none completed. Report completed_depth=3, the actual node count and that the next iteration was interrupted; do not claim a complete depth-4 minimax result.

**Repair task:** Integrate a decision job with a legal fallback and explicit completion status. Record how increasing the budget changes both response latency and decision quality. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 28.4: Learning systems, neural inference and responsible evaluation

### Question 1

**Prompt:** Why separate complete episodes across data splits?

**Answer guidance:** It reduces leakage from highly correlated examples belonging to the same episode.

### Question 2

**Prompt:** What mathematical rule underlies backpropagation?

**Answer guidance:** The chain rule applied through the computation graph.

### Question 3

**Prompt:** Why retain a rules-based baseline?

**Answer guidance:** It reveals whether learning adds useful quality relative to its data, runtime and maintenance costs.

### Question 4

**Prompt:** For x=(1,2), y=1, w=(0,0), b=0 and learning rate 0.1, compute one logistic cross-entropy gradient-descent update.

**Answer guidance:** p=0.5, so p-y=-0.5. The weight gradient is (-0.5,-1), bias gradient -0.5. Updated w=(0.05,0.10), b=0.05. The new logit is 0.30.

### Question 5

**Prompt:** A classifier scores 98% when frames are randomly split, but 72% when entire episodes are held out. Which estimate better supports new-episode use, and why?

**Answer guidance:** The held-out-episode result better matches the stated deployment question because correlated frames from the same episode no longer leak across the split. Report both methods, the class baseline and uncertainty rather than treating 98% as demonstrated generalization.

**Repair task:** Export a versioned model and feature schema, then integrate a bounded inference adapter with a rules fallback. Keep model output advisory; authoritative simulation still validates legal actions. Reattempt with one changed input or boundary condition and explain why the result differs.

## Module 28 review answers

### Review 1

**Prompt:** A* found a route, but the agent never reaches the target. Name four different layers to inspect.

**Answer guidance:** Navigation representation/clearance, path freshness, steering/progress detection and collision/physical execution. Also inspect target changes and action ownership. A graph path is not a guarantee of executable motion.

### Review 2

**Prompt:** How do hysteresis and action cancellation solve different AI problems?

**Answer guidance:** Hysteresis avoids unstable selection around similar scores; cancellation releases resources/ownership when an action stops. A stable selector can still leak requests, and perfect cleanup can still thrash between actions.

### Review 3

**Prompt:** A search expires before completing the first root move. What can it safely return?

**Answer guidance:** A legal fallback validated before expensive search, or a move from the last fully completed iteration. A partial score without a corresponding fully defined action is not safe. Terminal states need their own result.

### Review 4

**Prompt:** A classifier scores 99% after randomly splitting frames from the same matches. Why is that evidence weak?

**Answer guidance:** Closely related frames can leak episode-specific information across splits. Split independent episodes/scenarios before preprocessing and model selection, compare an appropriate baseline, and report held-out error categories and deployment costs.

### Review 5

**Prompt:** How should a learned component behave when the model fails to load or inference is too slow?

**Answer guidance:** Validate artifact/schema, use a tested bounded rules/legal-action fallback, emit diagnostics outside critical execution, and keep game progression available. Offline accuracy does not justify making an unbounded model dependency authoritative.

# Module 29: Multiplayer simulation and online services

## Lesson 29.1: Authority, prediction and reconciliation

### Question 1

**Prompt:** What is authoritative state?

**Answer guidance:** The state accepted as the deciding game truth under the chosen trust model.

### Question 2

**Prompt:** Which inputs are replayed after acknowledgment of input 40 in the example?

**Answer guidance:** Unacknowledged inputs 41 through 44.

### Question 3

**Prompt:** Why send intentions rather than unrestricted reward totals?

**Answer guidance:** The authority can validate and compute outcomes instead of trusting client-supplied benefits.

### Question 4

**Prompt:** Authority acknowledges input 40 at x=10. Pending inputs 41 through 44 each move +1. What is the reconciled prediction?

**Answer guidance:** Restore x=10 and replay only 41,42,43,44, producing x=14. Do not replay 40 or discard all pending input. The acknowledgment must be tied to the authoritative state after those acknowledged effects.

### Question 5

**Prompt:** Why is acknowledging the highest received sequence unsafe when an earlier input is missing?

**Answer guidance:** The client may discard the missing input even though the authority never applied it. A cumulative acknowledgment must refer to the highest contiguous processed sequence, or the protocol must explicitly describe selective acknowledgment and missing-input semantics.

**Repair task:** Create an engine command schema and separate authoritative, predicted and render-only state. Record one correction with the exact acknowledged and replayed input IDs. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 29.2: Snapshots, interpolation, relevance and lag compensation

### Question 1

**Prompt:** What cost does snapshot interpolation commonly add?

**Answer guidance:** Additional presentation delay from buffering earlier snapshots.

### Question 2

**Prompt:** Why must delta-compression baselines be identified?

**Answer guidance:** The receiver needs the correct prior state to reconstruct the delta.

### Question 3

**Prompt:** Why avoid transmitting irrelevant hidden enemy state?

**Answer guidance:** A modified client may inspect received information even if the normal UI hides it.

### Question 4

**Prompt:** Positions are 2 m at 1.00 s and 4 m at 1.10 s. What is the interpolated position at 1.04 s?

**Answer guidance:** alpha=(1.04-1.00)/(1.10-1.00)=0.4, so x=2+0.4*(4-2)=2.8 m. Use the simulation timestamps, not arrival times.

### Question 5

**Prompt:** A delta names baseline 120, but the receiver only retains baseline 121. Should it apply the delta to 121?

**Answer guidance:** No. The delta is meaningful only relative to its named baseline. Trigger the specified full-state or baseline recovery path and preserve a valid displayed state while recovering.

**Repair task:** Implement authority-side relevance filtering and capture the outgoing payload. Demonstrate that a hidden entity is absent from the unauthorized client, not merely invisible in the renderer. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 29.3: Lockstep, rollback and deterministic replay

### Question 1

**Prompt:** How much time do 120 ticks cover at 60 Hz?

**Answer guidance:** Two seconds.

### Question 2

**Prompt:** How much raw storage do 120 snapshots of 2 MB require?

**Answer guidance:** 240 MB.

### Question 3

**Prompt:** Why are external side effects difficult during rollback?

**Answer guidance:** Re-executing a tick must not repeat irreversible actions such as issuing a reward or sending an external message.

### Question 4

**Prompt:** With S_0=0 and predicted inputs [1,1,0,1], tick 2 is corrected to -1. Which state must be restored and what is the corrected S_4?

**Answer guidance:** Restore the pre-tick state S_2=2. Tick 2 gives S_3=1, and tick 3 gives S_4=2. Restoring S_3 would retain an effect of the incorrect prediction.

### Question 5

**Prompt:** A late input refers to a tick older than the snapshot ring. What is a valid response, and what is an invalid shortcut?

**Answer guidance:** Use a documented resynchronization, pause or disconnect policy. Applying the old input to the current tick or claiming rollback succeeded without the required state is invalid.

**Repair task:** Add a bounded rollback ring to your engine or a separate deterministic two-client demonstration. Keep irreversible side effects behind an explicit confirmation/idempotency boundary. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 29.4: Match services, identity, persistence and failure recovery

### Question 1

**Prompt:** Is authentication the same as authorization?

**Answer guidance:** No. Identity verification and permission to perform a specific action are separate checks.

### Question 2

**Prompt:** Why identify a match-result operation uniquely?

**Answer guidance:** Retries can then be recognized and processed without duplicating its durable effect.

### Question 3

**Prompt:** Must this lab use a paid public cloud?

**Answer guidance:** No. Local services and synthetic accounts satisfy the educational objective.

### Question 4

**Prompt:** A result commits, but its response is lost. The client retries with the same operation ID and payload. What must happen to the reward total?

**Answer guidance:** The durable effect must not be repeated. The service returns the prior result or an already-applied response, using an operation record committed atomically with the reward update.

### Question 5

**Prompt:** Why must a reused operation ID with a different payload be rejected instead of treated as a normal retry?

**Answer guidance:** An idempotency key identifies one operation, not arbitrary later edits. Accepting a changed payload can conceal corruption or unauthorized changes. Bind the ID to the canonical payload and report a conflict.

**Repair task:** Implement a file-backed local result store and prove exact retry behavior across a process restart. Add a match-state transition table and an unavailable-service client state. Reattempt with one changed input or boundary condition and explain why the result differs.

## Module 29 review answers

### Review 1

**Prompt:** The server receives inputs 10, 12 and 13 but not 11. What may it acknowledge under the contiguous-ACK protocol?

**Answer guidance:** After applying 10 it may acknowledge 10; 12 and 13 remain buffered until 11 arrives. Acknowledging 13 would make the client discard missing input 11 and break the replay contract.

### Review 2

**Prompt:** Is hiding an entity in the renderer sufficient to prevent clients from learning its position?

**Answer guidance:** No. The server must filter relevance before transmitting the state. Inspect payloads and account for related events/deltas; a client can inspect received data regardless of render visibility.

### Review 3

**Prompt:** Explain the off-by-one error in restoring S_(t+1) when replacing input I_t.

**Answer guidance:** With S_t defined before I_t, S_(t+1) already includes the old input. Restore S_t, apply the corrected I_t and replay later inputs. Starting after the old input preserves its effect or double-applies work.

### Review 4

**Prompt:** A reward committed but the response was lost. How does the client retry without duplicating the reward?

**Answer guidance:** Reuse the same operation ID and payload. In an atomic transaction, the service sees the recorded exact operation and returns its existing result/no-op. Reusing an ID with a different payload is a conflict.

### Review 5

**Prompt:** What does an in-process faulty-network test prove, and what remains to test?

**Answer guidance:** It tests the modeled protocol under deterministic delay/loss/reorder/duplicate scenarios. It does not test sockets, process isolation, real clock drift, bandwidth limits, production authentication or platform transport failures. Add separate integration tests.

# Module 30: Production quality and the undergraduate engine capstone

## Lesson 30.1: Profiling, frame budgets and performance regression tests

### Question 1

**Prompt:** What is the ideal frame time after a 10x speedup of the example 2 ms subsystem?

**Answer guidance:** 18 ms unchanged work plus 0.2 ms optimized work = 18.2 ms.

### Question 2

**Prompt:** Why record build type?

**Answer guidance:** Debug and optimized builds can have very different performance and checks.

### Question 3

**Prompt:** Why can a microbenchmark improvement fail to help the game?

**Answer guidance:** That operation may not dominate the real critical path or may create costs elsewhere.

### Question 4

**Prompt:** Using nearest-rank percentiles, what are the mean and p95 of [10,10,10,10,50] ms? Is this enough data to characterize a real game tail?

**Answer guidance:** The mean is 18 ms. ceil(0.95*5)=5, so p95 is 50 ms. Five observations only validate the calculation; a real tail claim needs a suitable workload, many samples and repeated runs.

### Question 5

**Prompt:** A 20 ms frame contains 2 ms of optimizable work. What is the ideal total time after a 10x improvement, and what is the infinite-speed lower bound?

**Answer guidance:** 18+2/10=18.2 ms after a 10x improvement. The modeled lower bound is 18 ms. This assumes the other work and critical-path structure stay unchanged.

**Repair task:** Add a reproducible capstone benchmark with raw frame durations, work counts and environment metadata. Keep measurement code out of the authoritative replay hash. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 30.2: Compatibility, accessibility, localization and human testing

### Question 1

**Prompt:** Why use pseudo-localization before full translation?

**Answer guidance:** It exposes layout and text-handling problems using expanded or altered test strings.

### Question 2

**Prompt:** What should a control prompt show after rebinding?

**Answer guidance:** The current binding, not an obsolete hard-coded default.

### Question 3

**Prompt:** Does checking every accessibility guideline prove legal compliance?

**Answer guidance:** No. It supports engineering review but is not a legal determination or substitute for user evaluation.

### Question 4

**Prompt:** After interact is rebound from E to Space, which systems must reflect the change?

**Answer guidance:** Gameplay input, visible prompts, relevant menus/help, and persisted settings must agree. Include a restart/reload test and a recovery path for conflicting or unusable bindings.

### Question 5

**Prompt:** Why is an expanded pseudo-localized label useful but insufficient to prove support for all languages?

**Answer guidance:** It exposes layout and hard-coded-string problems, but it does not test real translation quality, plural rules, shaping, grapheme behavior, locale formatting or right-to-left layout. State the actual tested language and layout scope.

**Repair task:** Centralize action bindings and text resources in the engine. Have an independent tester complete the loop with a changed binding and muted audio; record and retest actual issues. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 30.3: Packaging, patching, modding and supply-chain boundaries

### Question 1

**Prompt:** Can a data-only mod still be dangerous to robustness?

**Answer guidance:** Yes. Malformed sizes, structures or resource demands can trigger failures unless validated.

### Question 2

**Prompt:** Why separate saves from replaceable installation files?

**Answer guidance:** Updates or reinstalls should not erase user progress.

### Question 3

**Prompt:** Does naming a system a sandbox establish isolation?

**Answer guidance:** No. Isolation depends on the enforced capability, memory and resource boundaries.

### Question 4

**Prompt:** A texture declares 100000 by 100000 pixels at four bytes per pixel. What allocation would it imply, and when should it be rejected?

**Answer guidance:** It implies 40,000,000,000 bytes, about 40 GB decimal. Reject it during schema/resource validation before allocating, checking both individual dimensions and total package limits with overflow-safe arithmetic.

### Question 5

**Prompt:** Why does a SHA-256 checksum stored beside a downloaded archive not by itself prove publisher authenticity?

**Answer guidance:** An attacker able to replace the archive may also replace the checksum. A trusted channel, trusted expected digest or signature-verification chain is needed for authenticity. The digest still supports byte-integrity comparison against a trusted value.

**Repair task:** Create a versioned data-only mod schema and an actual release folder. Test rejected input, interrupted staging and a save that remains intact when installation files are replaced. Reattempt with one changed input or boundary condition and explain why the result differs.

## Lesson 30.4: Capstone review, release and technical postmortem

### Question 1

**Prompt:** What proves completion beyond a recorded demo?

**Answer guidance:** A reproducible package, tests, usable controls, documented limitations and independent execution.

### Question 2

**Prompt:** Why disclose library and AI assistance?

**Answer guidance:** It distinguishes the learner's decisions and understanding from supplied work and supports provenance.

### Question 3

**Prompt:** Why include a live modification in an oral review?

**Answer guidance:** It tests whether the learner can reason about and change the system rather than only present a prepared artifact.

### Question 4

**Prompt:** A game meets its frame budget but an ordinary interrupted save can corrupt the only progress file. Can a high overall rubric score override this?

**Answer guidance:** No. Data loss in a claimed supported path is a mandatory release blocker. Repair the path or explicitly remove the unsafe behavior, then test the resulting supported contract. A weighted score cannot waive critical correctness requirements.

### Question 5

**Prompt:** What should a technical postmortem contain beyond a list of completed features?

**Answer guidance:** Decisions, hypotheses, failed approaches, measurements, reproducible defects and fixes, user-test findings, limitations, provenance and assistance disclosures, and a reasoned account of what would change next. Claims should point to actual evidence.

**Repair task:** Archive the reviewed engine/game revision with a clean-build record, an independently completed loop, one reproduced regression and a live-change review. Do not mark human review complete in advance. Reattempt with one changed input or boundary condition and explain why the result differs.

## Module 30 review answers

### Review 1

**Prompt:** A release’s mean frame time improves but its p99 doubles. Is it necessarily better?

**Answer guidance:** No. State the target experience and budget, inspect raw distributions and stalls, and compare repeated runs plus correctness. Mean throughput and tail responsiveness are different outcomes.

### Review 2

**Prompt:** What is wrong with marking an untested platform as compatible because the code is portable?

**Answer guidance:** Portability intent is not execution evidence. Toolchains, devices, paths, fonts and timing can differ. Mark it untested until the declared build/launch/input scenarios are executed.

### Review 3

**Prompt:** Does a data-only mod eliminate security and reliability risk?

**Answer guidance:** No. Untrusted counts, dimensions, paths, decompression and schema versions can still exhaust resources or escape boundaries. Validate before allocation/use, cap actual bytes and avoid treating data-only as inherently safe.

### Review 4

**Prompt:** Why keep both a numerical rubric and mandatory release blockers?

**Answer guidance:** The rubric distinguishes quality across categories; blockers enforce non-negotiable correctness and review conditions. Excellent documentation cannot compensate for destructive saves or a reviewer unable to launch the game.

### Review 5

**Prompt:** What belongs in a technical postmortem beyond a feature list?

**Answer guidance:** Predictions versus measured outcomes, evidence-linked failures, corrected assumptions, rejected alternatives, remaining limitations, reproducible results and one bounded next improvement. Distinguish supplied demonstration results from the learner’s own engine evidence.


# Evaluating implementation work

Reference kernels are in starter/python/references. They solve the narrow contract, not the full lab or capstone. Compare behavior and invariants before comparing code style. Passing 98 supplied cases does not prove every possible input is safe. Extend tests for your engine’s scale, data and trust boundaries.

The five integration companions and C++ harness disclose their limits in NATIVE_INTEGRATION_GUIDE and evidence. Full lab answers include actual maintained-library, device, transport and human evidence that cannot be fabricated by an answer key. Grade an honest measured limitation more highly than an unsupported claim of completeness.
