# Worked answers and review guidance

Attempt every question and practical task before consulting this file. The first three questions in each lesson and their original answers are retained from the source curriculum. New application, review and written-problem solutions are marked by their identifiers. Alternative sound derivations may be accepted when assumptions are stated.


## Assessment and independent work
Each of the five lesson questions is scored 0-2: zero for absent/incorrect; one for a partly correct answer or a correct number without requested reasoning; two for a correct answer with the relevant argument. **Keep the original three-question threshold: questions 1-3 need at least 5/6. The full five-question quiz also needs at least 8/10.** Complete assigned study, the full practical assignment and the unaided transfer task before marking the lesson complete. Code-checker success alone is not completion.

The five module-review questions use the same two-point scale; suggested pass is 8/10. Correct missed work and solve a changed example. For the 15 written problems in each module, retain an independent attempt and a correction; proofs must identify assumptions and justified steps. At least two derivations/proofs per module must be reviewed, not merely checked for a final number.

The Gate B project uses the original 100-point rubric: correctness/requirements 30; tests/verification 25; reasoning/tradeoffs 15; quantitative error/performance analysis 10; reproducibility 10; communication/provenance 10. Suggested pass is 80/100, every essential check completed, and no unresolved critical defect in the claimed scope. A reviewer may accept another technically sound method when its assumptions and evidence are explicit.

Reference answers are study aids after an attempt. Explain all assisted code, record help received, and do the transfer task without following a supplied solution. Nothing here grants an academic credential. Passing a few numerical examples does not prove a mathematical theorem or demonstrate all of a semester's subject depth.

## Algebra bridge solutions

### A01
Solve 3x+2=14.

**Worked answer.** Subtract 2: 3x=12. Divide by 3: x=4. Substitution gives 14.

### A02
Solve 5-2x=11.

**Worked answer.** Subtract 5: -2x=6; divide by -2 to obtain x=-3.

### A03
Solve x/4+3=8.

**Worked answer.** Subtract 3 to get x/4=5; multiply by 4: x=20.

### A04
Solve 2(x-3)=10.

**Worked answer.** Divide by 2: x-3=5; add 3: x=8.

### A05
Solve (x+1)/3=(x-1)/2.

**Worked answer.** Multiply by 6: 2x+2=3x-3, so x=5. Both original denominators are nonzero constants.

### A06
Solve x^2=9 over the real numbers.

**Worked answer.** x=3 or x=-3. Both square to 9; taking only the positive square root loses a solution.

### A07
Solve x(x-4)=0.

**Worked answer.** By the zero-product rule, x=0 or x=4. Do not divide by x.

### A08
Solve 2^x=32.

**Worked answer.** 32=2^5, so x=5. Equivalently x=log2(32).

### A09
Solve sqrt(x-1)=3 and state the real domain.

**Worked answer.** The domain is x>=1. Squaring gives x-1=9 and x=10. It satisfies the original equation.

### A10
Solve d=v*t for t when d=18 m and v=3 m/s. State the forbidden denominator.

**Worked answer.** t=d/v=6 s. The rearrangement requires v!=0; the forward-travel exercise further requires v>0 and d>=0.

<!-- PAGEBREAK -->
# Module 06 — Worked answers

## Lesson 06.1 — Algebra, functions, logarithms and trigonometry

**06.1.Q1.** What is log2(64)?

**Answer:** 6, because 2^6 = 64.

**06.1.Q2.** Convert 180 degrees to radians.

**Answer:** pi radians.

**06.1.Q3.** What restriction applies when computing speed = distance/time?

**Answer:** Time cannot be zero; also state the physical units and whether negative time is meaningful.

**06.1.Q4.** State the real domain of f(x) = sqrt(x-2)/(x-5).

**Answer:** x >= 2 and x != 5. The square root and denominator impose separate conditions.

**06.1.Q5.** Solve x(x-2)=0 without losing a solution.

**Answer:** The zero-product rule gives x=0 or x=2. Dividing by x would silently remove x=0.

**Transfer task:** A unit moves at 8 m/s at 30 degrees for 0.5 s. Find its displacement in the stated y-up plane.

**Transfer answer:** Distance is 4 m; displacement is (4*cos(pi/6), 4*sin(pi/6)) = (2*sqrt(3), 2) m, approximately (3.464, 2). Its length is 4 m.

**Practical review:** Do not pass the number 90 directly to a radian-based sine function, cancel a possibly zero factor, or round a logarithm before defining the discrete problem. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_06_1.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 06.2 — Logic, sets and quantified claims

**06.2.Q1.** When is P -> Q false?

**Answer:** When P is true and Q is false.

**06.2.Q2.** Negate "every unit has positive health."

**Answer:** There exists a unit whose health is not positive.

**06.2.Q3.** Why must the domain of a quantified statement be explicit?

**Answer:** The claim can change meaning or truth when it ranges over different objects or inputs.

**06.2.Q4.** What are the truth values of "all elements are positive" and "some element is positive" on an empty set?

**Answer:** The universal statement is true; the existential statement is false. State an independent nonempty condition when required.

**06.2.Q5.** Does P -> Q imply Q -> P? Give a game counterexample.

**Answer:** No. Having a key may imply opening a door, while an unlocked door can open without a key.

**Transfer task:** Two players have allowed spawn sets {A} and {B}. Which quantifier order is satisfied?

**Transfer answer:** For every player, there exists an allowed spawn point. There is no single point allowed for every player, because the intersection is empty.

**Practical review:** Implication is not its converse. A validator passing a universal check on an empty collection does not establish that the collection is nonempty. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_06_2.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 06.3 — Proofs, induction and invariants

**06.3.Q1.** What are the two essential parts of induction?

**Answer:** A valid base case and an implication from the inductive hypothesis to the next case.

**06.3.Q2.** What is 1+...+100?

**Answer:** 100*101/2 = 5050.

**06.3.Q3.** Why does a mathematical proof not eliminate implementation tests?

**Answer:** The code, machine arithmetic or environmental assumptions may differ from the proven model.

**06.3.Q4.** Can a loop invariant be true while a loop never terminates?

**Answer:** Yes. A loop may preserve a property without decreasing a well-founded progress measure. Prove progress separately.

**06.3.Q5.** State a precise invariant after processing i health values.

**Answer:** The count equals the number of strictly positive entries in the prefix values[0:i], and 0<=i<=N.

**Transfer task:** Change "positive health" to "health at least 3." Which parts of the proof change?

**Transfer answer:** The counted predicate changes to h>=3, as does the condition in the preservation step. Initialization, the prefix structure, the decreasing N-i variant, and the termination argument are unchanged. Add tests at 2,3,4.

**Practical review:** A statement like "the count is correct" is too vague without saying which prefix, at what point in the loop, and under which health rule. Do not omit termination. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_06_3.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 06.4 — Counting, graphs and recurrences

**06.4.Q1.** How many combinations arise from five independent binary choices?

**Answer:** 2^5 = 32.

**06.4.Q2.** How many edges can a simple undirected graph with five vertices have?

**Answer:** 5*4/2 = 10.

**06.4.Q3.** Why is a dependency cycle a problem for a simple startup order?

**Answer:** No member can be initialized first while requiring another member of the cycle to be ready.

**06.4.Q4.** Four slots have three choices each; option A in both first slots is forbidden. How many loadouts remain?

**Answer:** 81-9=72. The last two slots still have 3*3 choices in each forbidden case.

**06.4.Q5.** Does the repeatedly sorted reference topological routine automatically have O(V+E) time?

**Answer:** No. The list operations and repeated sorting add costs beyond a queue-based linear-time model. Analyze the actual implementation.

**Transfer task:** There are six nodes. Compare the maximum directed and undirected edge counts without self-loops.

**Transfer answer:** The directed maximum is 6*5=30; the simple undirected maximum is 6*5/2=15 because each unordered pair is counted once.

**Practical review:** Do not multiply counts across coupled choices, add overlapping alternatives without correction, or equate recursion depth with total work. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_06_4.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

<!-- PAGEBREAK -->
## Module 06 — Written problem solutions

### 06.P01
A unit moves at 12 m/s for 0.25 s. Find distance, then solve for the time needed to travel 15 m at the same constant speed.

**Worked answer:** d=v*t=3 m. The second time is 15/12=1.25 s under the constant-speed/no-obstacle model.

### 06.P02
State the real domains of sqrt(9-x), 1/(x+2), and log2(x-1).

**Worked answer:** Respectively x<=9; x!=-2; and x>1. Each restriction comes from a different operation.

### 06.P03
Convert 30, 135, and -90 degrees to radians. Give the unit direction at -90 degrees in a y-up plane.

**Worked answer:** The angles are pi/6, 3pi/4, and -pi/2. The last direction is (0,-1).

### 06.P04
Compute log2(256), log10(1000), and the floor-halving count for 1000. Explain why the last is not rounded log2(1000).

**Worked answer:** The first two are 8 and 3. Floor-halving takes 9 steps. The recurrence uses floor at each division; rounding a real logarithm answers a different integer rule.

### 06.P05
Construct the truth table for P -> Q and for its converse. Which rows distinguish them?

**Worked answer:** For rows (P,Q)=(0,0),(0,1),(1,0),(1,1), implication is 1,1,0,1 and converse is 1,0,1,1. They differ on the two unequal rows.

### 06.P06
Negate: every living unit has some valid owner. Keep the living-unit domain explicit.

**Worked answer:** There exists a living unit with no valid owner. Equivalently, some living unit u has every candidate owner invalid for u. Negating only "valid" while keeping all quantifiers would be wrong.

### 06.P07
Prove that the sum of the first n odd positive integers is n^2 for n>=0.

**Worked answer:** Base n=0 gives empty sum 0. Assume the sum through 2k-1 is k^2. Add the next odd integer 2k+1: k^2+2k+1=(k+1)^2. Induction proves the claim.

### 06.P08
Prove that the sum of two odd integers is even. State your domain.

**Worked answer:** For integers a,b, write the odd numbers as 2a+1 and 2b+1. Their sum is 2(a+b+1), an even integer. The integer domain makes the parity definition applicable.

### 06.P09
Give a counterexample to each claim: every positive number is an integer; (a+b)^2=a^2+b^2 for all real a,b; a successful test proves all inputs correct.

**Worked answer:** Use 0.5 for the first. For the second, a=b=1 gives 4 on the left and 2 on the right. For the third, a function correct at input 0 but wrong at 1 can pass a single test at 0. The claims have different domains; state each counterexample precisely.

### 06.P10
A game offers 4 character classes, 3 weapons and 2 maps. One class cannot use one weapon on either map; all other choices are allowed. Count valid combinations.

**Worked answer:** Unrestricted total is 4*3*2=24. The forbidden class/weapon pair occurs on 2 maps, so 24-2=22 valid combinations.

### 06.P11
In a collection, 12 items are red, 9 are heavy, and 4 are both. How many are red or heavy?

**Worked answer:** 12+9-4=17. Subtract the overlap counted twice.

### 06.P12
For a simple undirected graph on 8 vertices, find the maximum number of edges. Contrast directed edges without self-loops.

**Worked answer:** Undirected: 8*7/2=28. Directed: 8*7=56, because each direction is distinct.

### 06.P13
Edges A->C, B->C, C->D, B->E mean prerequisites. Give two valid startup orders and one edge that creates a cycle.

**Worked answer:** A,B,C,D,E and B,A,E,C,D are valid. Adding D->A creates A->C->D->A. Other valid answers must respect every edge.

### 06.P14
For n=2^k, solve T(n)=T(n/2)+1 with T(1)=1.

**Worked answer:** Unroll k halvings to reach 1. T(n)=1+k=1+log2(n). This is an exact recurrence result for powers of two, not a runtime in seconds.

### 06.P15
For n=2^k, solve T(n)=2T(n/2)+n with T(1)=1.

**Worked answer:** Each of k nonleaf levels contributes n; there are n leaves contributing one each. T(n)=n*k+n=n*log2(n)+n. The depth is k but total work is not merely k.

## Module 06 — Review answers

**06.R1.** A new door opens with a key, or with both level>=7 and energy>=4. State a Boolean rule and the numeric boundary tests.

**Answer:** key OR (level>=7 AND energy>=4). Test level 6,7,8 and energy 3,4,5 with key false; key true separately demonstrates the override.

**06.R2.** Explain why an invariant and a decreasing variant have different roles.

**Answer:** The invariant establishes a preserved property supporting correctness; a nonnegative integer variant that strictly decreases supports termination.

**06.R3.** A log2 estimate says 9.97 steps. What must be specified before turning that into an integer loop count?

**Answer:** The exact discrete recurrence, rounding rule, starting cases, and stopping condition. Floor- and ceiling-halving differ.

**06.R4.** A startup graph has two independent prerequisites for a scene. Must there be only one valid order?

**Answer:** No. Independent prerequisites can appear in either order unless further edges constrain them.

**06.R5.** What evidence distinguishes a tested general claim from a proved one?

**Answer:** Tests document selected cases and environment. A proof supplies assumptions, a precise domain, and justified steps covering every case in the model; code-model correspondence still needs checking.

<!-- PAGEBREAK -->
# Module 07 — Worked answers

## Lesson 07.1 — Vectors, dot products and projections

**07.1.Q1.** What is the length of (6,8)?

**Answer:** 10.

**07.1.Q2.** What is the dot product of (1,0) and (0,1)?

**Answer:** 0, indicating perpendicular directions.

**07.1.Q3.** Why cannot the zero vector be normalized by the ordinary formula?

**Answer:** Its length is zero, so division is undefined and it has no unique direction.

**07.1.Q4.** Why does unnormalized input (1,1) make diagonal movement faster than input (1,0) at the same scalar multiplier?

**Answer:** Their lengths are sqrt(2) and 1. Normalize nonzero directional input when equal speed is the intended rule.

**07.1.Q5.** Compute the projection of (3,4) onto the nonunit vector (2,0).

**Answer:** ((6)/(4))*(2,0)=(3,0). The b·b denominator is required.

**Transfer task:** Find the projection of v=(2,2) onto b=(1,1), and then the rejection v-projection.

**Transfer answer:** v·b=4 and b·b=2, so projection=2*(1,1)=(2,2). The rejection is (0,0), because v is already parallel to b.

**Practical review:** Zero dot product does not establish two useful perpendicular directions when one operand is zero. Do not confuse a scalar component with a projection vector. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_07_1.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 07.2 — Matrices, bases and linear systems

**07.2.Q1.** Do matrices generally satisfy AB = BA?

**Answer:** No. Transformation order usually changes the result.

**07.2.Q2.** What happens to invertibility when an axis is scaled to zero?

**Answer:** Information on that axis is lost, making the transformation singular.

**07.2.Q3.** Why solve Ax=b without explicitly forming an inverse?

**Answer:** Factorization can be more efficient and numerically preferable, especially for repeated or large solves.

**07.2.Q4.** What are the output dimensions of a 3x2 matrix times a 2x4 matrix?

**Answer:** 3x4. The inner dimension 2 is summed over.

**07.2.Q5.** Give two different points that a zero x-scale maps to the same point.

**Answer:** For diag(0,1), (1,2) and (7,2) both become (0,2). Information along x is lost.

**Transfer task:** Solve x+y=2 and 2x+2y=5. What fails?

**Transfer answer:** Doubling the first equation requires 2x+2y=4, contradicting 5. The system has no solution; it is not a case of choosing a different inverse.

**Practical review:** Row storage order in memory does not determine whether the mathematics uses row or column vectors. Keep representation, multiplication convention, and composition order separate. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_07_2.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 07.3 — Homogeneous transforms, cameras and quaternions

**07.3.Q1.** Why commonly use w=0 for directions?

**Answer:** Translation should not change a pure direction; the homogeneous form makes the translation term vanish.

**07.3.Q2.** What does the view transform do?

**Answer:** It expresses world-space geometry in the camera coordinate system.

**07.3.Q3.** Why document multiplication order even when using a library?

**Answer:** The library convention and application convention must agree; otherwise valid arithmetic produces the wrong geometry.

**07.3.Q4.** Why do q and -q require care during quaternion interpolation?

**Answer:** They encode the same rotation but their raw component average is zero. Choose compatible signs before normalized interpolation.

**07.3.Q5.** For a rigid pose C=T(c)R, what is the view transform?

**Answer:** V=C^-1=R^T T(-c), with the inverse operations in reversed order.

**Transfer task:** A camera has no rotation and sits at (0,0,5). Where does world point (1,2,3) appear in camera coordinates?

**Transfer answer:** The view translation subtracts the camera position, producing (1,2,-2). This statement does not yet declare which camera-forward convention a future projection uses.

**Practical review:** Do not mix the terminal grid y-down convention with the geometry y-up convention, treat a direction as w=1, or confuse the camera pose with its inverse view transform. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_07_3.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 07.4 — Eigenvalues, least squares and singular values

**07.4.Q1.** What are the eigenvalues of diag(3,2)?

**Answer:** 3 and 2, with the coordinate axes as eigenvector directions.

**07.4.Q2.** What objective does ordinary least squares minimize?

**Answer:** The sum of squared residuals under its specified model.

**07.4.Q3.** Can a stable algorithm make an ill-conditioned problem insensitive?

**Answer:** No. It can limit added numerical error but cannot eliminate the problem's inherent sensitivity.

**07.4.Q4.** Can a 90-degree planar rotation have a nonzero real eigenvector?

**Answer:** No. It turns every real direction to a perpendicular one; no nonzero real vector remains on its original line.

**07.4.Q5.** Why does fitting a slope fail when every xi is equal?

**Answer:** Sxx=0, so the data contain no predictor variation to identify a unique slope separately from the intercept.

**Transfer task:** For diag(4,0.25), find the singular values, two-norm condition number, and two updates of (1,1).

**Transfer answer:** The singular values are 4 and 0.25; the condition number is 16. Two updates give (16,0.0625).

**Practical review:** Singular values are not generally signed eigenvalues. A tiny residual, visually good fit, or stable implementation cannot by itself remove an ill-conditioned problem. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_07_4.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

<!-- PAGEBREAK -->
## Module 07 — Written problem solutions

### 07.P01
Find displacement and distance from (2,-1,3) to (5,3,3).

**Worked answer:** Displacement is (3,4,0), and Euclidean distance is sqrt(9+16)=5.

### 07.P02
Normalize (-6,8) and check its squared length.

**Worked answer:** Length is 10; unit vector (-0.6,0.8) has squared length 0.36+0.64=1.

### 07.P03
Project v=(4,2) onto b=(1,1). Find the perpendicular residual.

**Worked answer:** v·b=6 and b·b=2, so projection=(3,3), residual=(1,-1). Its dot product with b is zero.

### 07.P04
For unit facing (1,0), compare displacements (1,1),(-1,1),(0,2) against an inclusive 45-degree field of view.

**Worked answer:** (1,1) lies exactly on the 45-degree boundary and passes; (-1,1) is at 135 degrees and fails; (0,2) is at 90 degrees and fails. Normalize or include both lengths in the threshold formula.

### 07.P05
Prove that v-((v·b)/(b·b))b is perpendicular to nonzero b.

**Worked answer:** Dot the residual with b: v·b-((v·b)/(b·b))*(b·b)=0. The nonzero premise ensures b·b>0 in the Euclidean real-vector setting.

### 07.P06
Prove that an orthonormal matrix Q preserves Euclidean squared length.

**Worked answer:** Because Q^T Q=I, ||Qv||^2=(Qv)^T(Qv)=v^T Q^T Qv=v^T v. This is a mathematical statement; finite arithmetic warrants tolerance tests.

### 07.P07
Multiply [[1,2],[3,4]] by [[2,0],[1,2]].

**Worked answer:** The result is [[4,4],[10,8]]: each entry is a row-column dot product.

### 07.P08
Solve x+2y=5 and 3x-y=1 by elimination.

**Worked answer:** From the first x=5-2y. Substitute: 15-6y-y=1, so y=2 and x=1. Verify both original equations.

### 07.P09
Give a nonzero nullspace vector of [[1,2],[2,4]], and state its rank.

**Worked answer:** (-2,1) maps to zero; the second row is twice the first, and a row is nonzero, so rank is 1.

### 07.P10
For column vectors, apply child translation (3,0,0) under parent T(5,1,0)*Rz(pi/2). Find the child origin in world space.

**Worked answer:** The child offset rotates from (3,0,0) to (0,3,0), then translates to (5,4,0).

### 07.P11
A no-rotation camera sits at (2,3,4). Find the view coordinates of world point (5,7,10), and of direction (1,0,0).

**Worked answer:** Subtract the camera translation from the point to get (3,4,6). The direction remains (1,0,0); translations do not affect w=0 vectors.

### 07.P12
Derive slope and intercept for ordinary least squares with an intercept.

**Worked answer:** Differentiate S=sum(yi-a*xi-b)^2. The b equation gives b=ybar-a*xbar. Substitute into the a equation to obtain a=sum((xi-xbar)(yi-ybar))/sum((xi-xbar)^2), requiring a positive denominator for uniqueness.

### 07.P13
Find the scalar-first quaternion for a 180-degree rotation around +z. Rotate (1,0,0).

**Worked answer:** q=(cos(pi/2),0,0,sin(pi/2))=(0,0,0,1) in exact arithmetic. The rotated vector is (-1,0,0).

### 07.P14
For A=[[3,0],[4,0]], find the singular values and rank using A^T A.

**Worked answer:** A^T A=[[25,0],[0,0]]. Its eigenvalues are 25 and 0, so the singular values are 5 and 0. Rank is 1. This differs from simply taking the magnitudes of A eigenvalues.

### 07.P15
For A=diag(1,10^-6), compare solutions for b=(1,0) and b_changed=(1,10^-6). What is the two-norm condition number?

**Worked answer:** The solutions are (1,0) and (1,1). A small change in b creates a unit change in one solution component. The condition number is 1/(10^-6)=10^6.

## Module 07 — Review answers

**07.R1.** How can an inverse round-trip test pass despite a convention error?

**Answer:** The forward and inverse routines can share compensating mistakes. Include independently derived points and rotations, not only mutual agreement.

**07.R2.** When should normalization fail instead of inventing a direction?

**Answer:** For a zero vector under the chosen math contract. The application may explicitly select a stationary or prior-orientation policy outside that routine.

**07.R3.** What does a nonzero vector in the nullspace tell you geometrically?

**Answer:** Distinct inputs separated by that vector share an output. The map loses information in that direction.

**07.R4.** Explain the difference among residual, forward error, and conditioning.

**Answer:** Residual measures Ax-b; forward error measures distance to a reference solution; conditioning measures solution sensitivity to input perturbations. Small residual can coexist with appreciable forward error in a sensitive problem.

**07.R5.** A child is positioned by M_parent*M_child. Why cannot the factors be swapped casually?

**Answer:** They map between different spaces, and matrix multiplication generally does not commute. The swapped product encodes a different sequence and often different geometric meaning.

<!-- PAGEBREAK -->
# Module 08 — Worked answers

## Lesson 08.1 — Limits, derivatives and rates

**08.1.Q1.** Differentiate x(t)=3*t*t.

**Answer:** dx/dt = 6*t.

**08.1.Q2.** What units does acceleration have when position is in meters?

**Answer:** Meters per second squared.

**08.1.Q3.** Why can excessively small finite-difference steps be inaccurate?

**Answer:** Subtracting nearly equal floating-point values magnifies rounding and cancellation error.

**08.1.Q4.** Differentiate (2t+1)^3.

**Answer:** 6(2t+1)^2 by the chain rule; the inner derivative contributes a factor of 2.

**08.1.Q5.** Why is |t| not differentiable at t=0?

**Answer:** The one-sided slopes are -1 and +1, so no common derivative limit exists.

**Transfer task:** For x(t)=(3t-1)^2, derive velocity and acceleration, then evaluate at t=1.

**Transfer answer:** x prime is 2(3t-1)*3=6(3t-1); x double prime is 18. At t=1, velocity=12 and acceleration=18 in the consistent derived units.

**Practical review:** The smallest perturbation is not automatically the most accurate. A numerical slope at a corner is not proof that an ordinary derivative exists. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_08_1.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 08.2 — Integrals, accumulation and continuous probability

**08.2.Q1.** Integrate constant velocity 5 over two seconds.

**Answer:** Displacement is 10 units of length.

**08.2.Q2.** What is the integral of 2*t from 0 to 3?

**Answer:** [t^2] from 0 to 3 = 9.

**08.2.Q3.** Why can an integral be zero despite nonzero motion?

**Answer:** Positive and negative displacement can cancel; total distance is a different quantity.

**08.2.Q4.** Can a probability density equal 2 without violating probability bounds?

**Answer:** Yes. A uniform density of 2 on an interval of length 0.5 integrates to one. Interval probabilities, not density heights, must lie in [0,1].

**08.2.Q5.** What is the integral of t^2 from 1 to 0?

**Answer:** -1/3. Reversing the integration limits negates the signed integral.

**Transfer task:** Velocity is +2 m/s for one second and -2 m/s for the next second. Find displacement and distance.

**Transfer answer:** Displacement is 2*1 + (-2)*1 = 0 m. Distance is |2|*1+|-2|*1 = 4 m.

**Practical review:** A density is not a probability at a point. Net displacement is not total distance, and multiplying final velocity by total time is not a general integration rule. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_08_2.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 08.3 — Newtonian mechanics and differential equations

**08.3.Q1.** What acceleration results from 10 N on a 2 kg mass?

**Answer:** 5 m/s^2.

**08.3.Q2.** How does impulse differ from force?

**Answer:** Impulse is force integrated over time and changes momentum; force is a rate of momentum change.

**08.3.Q3.** Why must initial conditions accompany a differential equation?

**Answer:** Many trajectories can satisfy the same differential rule; initial state selects the intended one.

**08.3.Q4.** Write the state equations for a linear damped spring about x=0.

**Answer:** dx/dt=v and dv/dt=(-k*x-c*v)/m, with m>0 and stated stiffness/damping conventions.

**08.3.Q5.** What is dE/dt for the ideal linear damped spring?

**Answer:** -c*v^2. Differentiate 0.5*m*v^2+0.5*k*x^2 and substitute the equations of motion.

**Transfer task:** A 2 kg body receives a 3 N*s impulse. What velocity change results? Compare with 3 N applied for 0.5 s.

**Transfer answer:** The impulse gives delta_v=3/2=1.5 m/s. The force over 0.5 s gives J=1.5 N*s and delta_v=0.75 m/s.

**Practical review:** Force is not velocity, mass is not weight, and energy conservation belongs first to a declared continuous model. Numerical damping or growth must be measured rather than hidden. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_08_3.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 08.4 — Time integration, stability and error

**08.4.Q1.** Which velocity does semi-implicit Euler use for the position update?

**Answer:** The newly updated velocity.

**08.4.Q2.** Does a fixed timestep guarantee a stable simulation?

**Answer:** No. Stability still depends on the equations, method and step size.

**08.4.Q3.** What is a useful check beyond watching the animation?

**Answer:** Compare to an analytic solution or conserved quantity and perform timestep-refinement tests.

**08.4.Q4.** For explicit Euler on an undamped spring, what is the one-step energy factor?

**Answer:** 1+omega^2*h^2. It exceeds one for positive h and nonzero omega.

**08.4.Q5.** Why must a refinement study hold the final physical time fixed?

**Answer:** Otherwise different step sizes simulate different problems, so their final-state errors are not directly comparable.

**Transfer task:** For m=1,k=25 and an undamped spring, what open interval of positive h satisfies the derived semi-implicit condition?

**Transfer answer:** omega=sqrt(25)=5, so 0<5h<2 gives 0<h<0.4 seconds. This is the stated linear undamped model, not a universal timestep rule.

**Practical review:** Equal step counts are not equal simulation durations. Smoothness is not accuracy, and a fixed step does not make an unstable update stable. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_08_4.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

<!-- PAGEBREAK -->
## Module 08 — Written problem solutions

### 08.P01
Differentiate 4t^3-2t+7, then evaluate the derivative at t=2.

**Worked answer:** Derivative is 12t^2-2; at 2 it is 46.

### 08.P02
Differentiate sin(3t) and explain the extra factor.

**Worked answer:** Derivative is 3*cos(3t). The factor 3 is the derivative of the inner function 3t; angles are in radians.

### 08.P03
For x(t)=t^3 meters, find velocity and acceleration at t=2 seconds.

**Worked answer:** v=3t^2=12 m/s and a=6t=12 m/s^2, with the coefficient interpreted in consistent units.

### 08.P04
Compute the forward difference of t^2 at t=3 with h=0.2 and its error versus the derivative.

**Worked answer:** ((3.2)^2-9)/0.2=6.2; the exact derivative is 6, so signed error is +0.2.

### 08.P05
Derive the centered-difference error for f(t)=t^3.

**Worked answer:** Expand (t+h)^3-(t-h)^3=6t^2h+2h^3. Divide by 2h to get 3t^2+h^2. The signed exact-arithmetic error is h^2.

### 08.P06
Integrate 3t^2 from 0 to 2.

**Worked answer:** The antiderivative is t^3. The definite integral is 8-0=8 in the resulting units.

### 08.P07
Use two-panel trapezoids to integrate t^2 on [0,1]. Compare to the exact result.

**Worked answer:** h=0.5. Estimate=0.5*(0/2+0.25+1/2)=0.375. Exact=1/3, so error=1/24, approximately 0.041667.

### 08.P08
Derive the constant-acceleration position formula from dx/dt=v and dv/dt=a.

**Worked answer:** Integrate the second equation with v(0)=v0: v=v0+at. Integrate again with x(0)=x0: x=x0+v0t+0.5at^2. State constant a and the initial conditions.

### 08.P09
A particle starts at x0=2 m with v0=3 m/s under a=-2 m/s^2. Find x and v at t=2 s.

**Worked answer:** v=3-4=-1 m/s. x=2+6-4=4 m. Being to the right of the start does not mean its current velocity is positive.

### 08.P10
A 4 kg body receives force 12 N for 0.5 s. Find acceleration, impulse and velocity change.

**Worked answer:** a=3 m/s^2, J=12*0.5=6 N*s, delta_v=J/m=1.5 m/s.

### 08.P11
For m=2,k=18,c=0, find omega and the continuous period.

**Worked answer:** omega=sqrt(18/2)=3 rad/s; period=2*pi/3 seconds, approximately 2.094.

### 08.P12
For x=1,v=2,a=-4 and h=0.1, compare explicit and semi-implicit one-step updates when acceleration is constant.

**Worked answer:** Both give v_new=1.6. Explicit gives x_new=1.2; semi gives x_new=1.16. The exact position is 1+0.2-0.02=1.18.

### 08.P13
Prove dE/dt=-c*v^2 for E=0.5*m*v^2+0.5*k*x^2 and the damped spring equations.

**Worked answer:** Differentiate: dE/dt=m*v*vprime+k*x*xprime. Substitute xprime=v and m*vprime=-k*x-c*v: cross terms -k*x*v+k*x*v cancel, leaving -c*v^2.

### 08.P14
For an undamped spring, derive the explicit Euler one-step energy ratio.

**Worked answer:** Substitute x_new=x+h*v and v_new=v-h*omega^2*x into E. Use k=m*omega^2; the mixed terms cancel. E_new=(1+omega^2*h^2)*E. For nonzero E this is the ratio.

### 08.P15
At fixed T=N*h under constant acceleration, derive explicit Euler position error relative to the analytic solution.

**Worked answer:** The numerical displacement is N*h*v0+a*h^2*sum(i for i=0..N-1)=v0*T+0.5*a*(T^2-T*h). Subtracting the exact displacement gives -0.5*a*T*h, a first-order error in h at fixed T.

## Module 08 — Review answers

**08.R1.** What is wrong with comparing 100 steps at two different h values as the same final-time experiment?

**Answer:** They represent different durations T=100h. Adjust step count so both runs reach the same physical horizon.

**08.R2.** A centered derivative estimate for |t| at zero is zero. Does that prove differentiability?

**Answer:** No. The left and right derivative limits disagree. Symmetric cancellation in the finite difference hides the corner.

**08.R3.** Name three errors that reducing h may not fix.

**Answer:** Omitted physics/model bias, noisy input measurements, and an implementation error; sufficiently small h may also worsen roundoff.

**08.R4.** For m=1,k=100 and h=0.25, evaluate the stated semi-implicit oscillator condition.

**Answer:** omega=10, so omega*h=2.5>2. It is outside the derived stable interval for the linear undamped oscillator.

**08.R5.** What should a simulator report after nonfinite values appear?

**Answer:** An explicit failure with the model, method, timestep, first failing step, and prior finite evidence. It must not label the trajectory converged or silently discard the failure.

<!-- PAGEBREAK -->
# Module 09 — Worked answers

## Lesson 09.1 — Probability and conditional reasoning

**09.1.Q1.** What is the probability of two independent events with probabilities 0.5 and 0.2 both occurring?

**Answer:** 0.1, the product under the stated independence assumption.

**09.1.Q2.** Is P(A|B) generally equal to P(B|A)?

**Answer:** No. They condition on different populations.

**09.1.Q3.** Why do rare-event base rates matter for an alert?

**Answer:** Even a small false-positive rate can produce many alerts when true events are very rare.

**09.1.Q4.** What is the probability of at least one success in three independent trials with p=0.5?

**Answer:** 1-(1-0.5)^3=7/8. The calculation assumes independent trials with the same success probability.

**09.1.Q5.** When is P(bug|alert) undefined in the detector model?

**Answer:** When P(alert)=p*s+(1-p)*f=0, because conditioning would divide by zero.

**Transfer task:** Keep sensitivity 0.9 and false-positive rate 0.05, but change the prior bug probability to 0.1. Find P(bug|alert).

**Transfer answer:** The true-alert probability is 0.09 and false-alert probability 0.9*0.05=0.045. The posterior is 0.09/0.135=2/3, much larger because the base rate changed.

**Practical review:** An alert rate, sensitivity, false-positive rate, and positive predictive probability are different quantities. Do not swap their denominators or assume independence from temporal separation. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_09_1.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 09.2 — Random variables, distributions and sampling

**09.2.Q1.** What is the expectation of 20 with probability 0.25 and 0 otherwise?

**Answer:** 5.

**09.2.Q2.** Does an expectation of 5 guarantee a reward of 5 on a trial?

**Answer:** No. It describes an average under the model, not an individual outcome.

**09.2.Q3.** Why separate random streams for unrelated systems?

**Answer:** An extra draw in one system should not unintentionally alter another system's sequence.

**09.2.Q4.** Under the specified weighted intervals, which category contains u=0.70 for weights (70,25,5)?

**Answer:** The second category, index 1, because the first interval excludes its upper endpoint.

**09.2.Q5.** Does linearity of expectation require independent variables?

**Answer:** No. Expectations add under their existence assumptions. Variances need covariance terms unless the relevant covariance is zero.

**Transfer task:** If two rewards are perfectly copied from one another, each with variance s^2, what is the variance of their sum?

**Transfer answer:** The sum is 2X, so its variance is 4s^2, not 2s^2. The covariance contributes the missing 2s^2.

**Practical review:** An expected value is not a per-trial guarantee. Setting a seed does not establish statistical independence, unbiased sampling, or security. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_09_2.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 09.3 — Inference, uncertainty and benchmark design

**09.3.Q1.** Why can adjacent frame times violate an independence assumption?

**Answer:** They share workload phases, caches, thermal state and other correlated conditions.

**09.3.Q2.** Does a small p-value establish a large useful improvement?

**Answer:** No. Statistical evidence and practical effect size are different questions.

**09.3.Q3.** Why report a tail percentile alongside a mean?

**Answer:** It exposes slow cases that can affect responsiveness despite an acceptable average.

**09.3.Q4.** For nineteen 5 ms samples and one 100 ms sample, what is nearest-rank p95?

**Answer:** 5 ms because ceil(0.95*20)=19. Report the maximum/p99 and sample count so the slow case is not hidden.

**09.3.Q5.** What does a p-value not tell you about an optimization?

**Answer:** It is not the probability the null is true, does not establish causality, and does not quantify practical effect size.

**Transfer task:** A is 5 ms and B is 4 ms in each paired run. What sign does B-A have, and what does that sign mean?

**Transfer answer:** The difference is -1 ms: B took less time in those pairs. The sign convention must remain the same throughout plots, intervals, and conclusions.

**Practical review:** Do not treat correlated frames as independent trials, label a sample maximum a well-estimated p99, or interpret statistical significance as a useful speedup. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_09_3.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 09.4 — Regression, correlation and ethical telemetry

**09.4.Q1.** Why is training-set fit alone insufficient?

**Answer:** A model can overfit and fail on new observations or workloads.

**09.4.Q2.** What is a confounder?

**Answer:** A variable that influences both the proposed explanatory factor and the outcome, complicating causal interpretation.

**09.4.Q3.** Why should telemetry collect only what the question requires?

**Answer:** It reduces privacy exposure and unnecessary data handling while keeping the experiment focused.

**09.4.Q4.** Predictions are [2,4] and observations [3,4]. What is RMSE?

**Answer:** sqrt((1^2+0^2)/2)=sqrt(0.5), approximately 0.707107 in the response units.

**09.4.Q5.** What simple baseline should accompany a fitted performance model?

**Answer:** For example, predict the training-response mean on held-out observations. Compare the same held-out error metric for both models.

**Transfer task:** Why is randomly splitting adjacent frames from one run into training and test sets potentially misleading?

**Transfer answer:** Both sets can share the same run-specific workload, cache, and timing structure. The test then measures similarity within a run rather than transfer to independent runs or scenes.

**Practical review:** Perfect training fit is not independent evaluation. A correlated predictor is not necessarily the cause, and synthetic timings must not be reported as observed machine results. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_09_4.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

<!-- PAGEBREAK -->
## Module 09 — Written problem solutions

### 09.P01
Two independent events have probabilities 0.3 and 0.4. Find the probability both occur and the probability at least one occurs.

**Worked answer:** Both=0.12. At least one=0.3+0.4-0.12=0.58, equivalently 1-0.7*0.6.

### 09.P02
A success probability is 0.1 on each of three independent trials. Find the probability of at least one success.

**Worked answer:** 1-(0.9)^3=0.271. A changing probability or dependence invalidates this exact model.

### 09.P03
A table has 80 true alerts and 120 false alerts. There are 100 actual bugs. Compute precision-like P(bug|alert) and sensitivity.

**Worked answer:** P(bug|alert)=80/(80+120)=0.4. Sensitivity=80/100=0.8. Their populations differ.

### 09.P04
With prior=0.02, sensitivity=0.9 and false-positive rate=0.1, compute P(bug|alert).

**Worked answer:** True-alert probability=0.018; false-alert probability=0.98*0.1=0.098. Posterior=0.018/0.116=9/58, approximately 0.155172.

### 09.P05
Derive the detector Bayes formula from conditional probability and a partition into bug/no-bug.

**Worked answer:** P(bug and alert)=P(bug)*P(alert|bug)=p*s. Total probability gives P(alert)=p*s+(1-p)*f. Divide the joint by total alert probability, requiring a positive denominator.

### 09.P06
A reward is 0 with probability 0.8 and 10 with probability 0.2. Find expectation and variance.

**Worked answer:** E[X]=2. E[X^2]=20. Var(X)=20-4=16; standard deviation is 4 reward units.

### 09.P07
Find mean and variance of a binomial success count with n=20,p=0.25.

**Worked answer:** Mean=np=5 and variance=np(1-p)=3.75, assuming independent identical-probability trials.

### 09.P08
Partition [0,1) for weights [1,0,3]. Which category contains u=0.25?

**Worked answer:** Intervals are [0,0.25) for index 0, empty for index 1, and [0.25,1) for index 2. Exactly 0.25 selects index 2.

### 09.P09
Prove E[X+Y]=E[X]+E[Y] for a finite joint distribution without assuming independence.

**Worked answer:** Sum (x+y)*P(X=x,Y=y) over all x,y. Distribute the sum, then sum the joint over y or x to obtain the marginal probabilities. The resulting terms are E[X] and E[Y]; factorization is unnecessary.

### 09.P10
For samples [1,2,3,4,100], find mean, median and nearest-rank p80 and p95.

**Worked answer:** Mean=110/5=22; median=3. p80 rank=ceil(4)=4 gives 4. p95 rank=ceil(4.75)=5 gives 100. State that these are sample summaries with n=5.

### 09.P11
For [2,2,4,4], compute sample mean, sample variance and standard error of the mean.

**Worked answer:** Mean=3. Squared deviations sum to 4; sample variance=4/(4-1)=4/3. Standard error=sqrt((4/3)/4)=sqrt(1/3), approximately 0.577350 under the model.

### 09.P12
Explain the 95% frequentist confidence-interval interpretation without assigning probability to a fixed realized parameter.

**Worked answer:** Under repeated datasets from the assumed sampling process, approximately 95% of intervals produced by the method contain the fixed true parameter. A particular realized interval either contains it or does not. Violated assumptions can change coverage.

### 09.P13
A benchmark runs A only on a cool machine and B only after a long heavy workload. What is confounded, and how could the design improve?

**Worked answer:** Algorithm is entangled with machine state/order. Use controlled warmup, randomized A/B ordering within matched workload blocks, multiple runs, and preserved raw data; evaluate residual state effects rather than assuming randomization removes everything.

### 09.P14
Fit y=a*x+b to points (0,1),(1,3),(2,5). Predict at x=3; the held-out observed value is 8. Give the residual.

**Worked answer:** The exact training line is a=2,b=1. Prediction is 7; observed-minus-predicted residual is +1. The point x=3 lies outside the training range, so identify extrapolation.

### 09.P15
Show that variance of the average of n independent identically distributed variables with finite variance s^2 is s^2/n.

**Worked answer:** Var(sum Xi)=n*s^2 when covariances vanish. Scaling by 1/n squares that factor: Var((sum Xi)/n)=n*s^2/n^2=s^2/n. Dependence adds covariance terms.

## Module 09 — Review answers

**09.R1.** A detector is 90% sensitive. Is an alert a 90% chance of a bug?

**Answer:** Not generally. The posterior also depends on the base rate and false-positive probability, through Bayes rule.

**09.R2.** What changes when you add an extra draw to a shared pseudorandom stream?

**Answer:** All subsequent consumers can receive different values. Separate controlled streams when unrelated subsystem behavior must remain independent of that call count.

**09.R3.** Why is a tiny p-value not sufficient evidence that a player will notice an improvement?

**Answer:** Statistical evidence is distinct from effect size, the relevant latency tail, end-to-end impact, and actual usability requirements.

**09.R4.** What is wrong with treating synthetic frame data as a hardware benchmark?

**Answer:** The values were generated by a chosen model rather than measured execution. They can teach analysis but cannot support a claim about a device.

**09.R5.** Name the minimum evidence for your own comparison experiment.

**Answer:** Correctness checks, workload and versions, included/excluded work, warmup and ordering, raw repeated trials with units, analysis script, uncertainty assumptions, and scope/limitations.

<!-- PAGEBREAK -->
# Module 10 — Worked answers

## Lesson 10.1 — Multivariable calculus and gradients

**10.1.Q1.** What is the gradient of x*x + 3*y*y?

**Answer:** (2*x, 6*y).

**10.1.Q2.** What does a Jacobian describe?

**Answer:** The first-order local mapping from small input changes to output changes for a vector-valued function.

**10.1.Q3.** Does a zero gradient always identify a minimum?

**Answer:** No. It may identify a maximum, saddle or other stationary point.

**10.1.Q4.** What is the Jacobian of F(x,y)=(x^2+y,xy)?

**Answer:** [[2x,1],[y,x]], with output components indexing rows and input components indexing columns.

**10.1.Q5.** Classify the origin for f=x^2-y^2.

**Answer:** It is a stationary saddle: f increases along the x axis and decreases along the y axis.

**Transfer task:** For the y-up height field h(x,z)=x^2+z^2, find a unit surface normal at (x,z)=(1,0).

**Transfer answer:** The unnormalized normal is (-2,1,0); divide by sqrt(5) to get (-2/sqrt(5),1/sqrt(5),0). The sign is chosen to give a positive y component.

**Practical review:** A gradient is local and coordinate-dependent. A zero gradient can describe a saddle or maximum, and a correct gradient does not make every step size safe. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_10_1.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 10.2 — Sampling, aliasing and Fourier ideas

**10.2.Q1.** What is the Nyquist frequency at 48,000 samples/second?

**Answer:** 24,000 Hz, the half-sampling-rate boundary; practical filtering requires additional care.

**10.2.Q2.** Why filter before downsampling?

**Answer:** To remove frequencies that would fold into misleading lower frequencies at the new sample rate.

**10.2.Q3.** Can post-filtering always undo aliasing?

**Answer:** No. Distinct original signals may already have become indistinguishable in the samples.

**10.2.Q4.** Why is sampling exactly at twice a sinusoid frequency risky for phase information?

**Answer:** At some phases the samples can all be zero, such as sin(pi*n). The boundary does not preserve arbitrary phase in the intended reconstruction sense.

**10.2.Q5.** What distinguishes spectral leakage from aliasing?

**Answer:** Leakage is spreading caused by finite-window/bin mismatch; aliasing is indistinguishability of different frequencies at the sampling rate.

**Transfer task:** A cosine at 700 Hz is sampled at 1000 Hz. Find its baseband alias magnitude and explain a sine caveat.

**Transfer answer:** The magnitude is 300 Hz. Cosine samples match positive 300 Hz; the 700 Hz sine samples are the negative of the 300 Hz sine samples for the stated zero phase.

**Practical review:** Do not confuse aliasing with random noise or spectral leakage, omit the sine phase inversion, or claim a two-tap average is a universal reconstruction filter. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_10_2.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 10.3 — Convolution, filters and systems

**10.3.Q1.** What does convolving with an impulse reveal?

**Answer:** The filter's impulse response, including its alignment convention.

**10.3.Q2.** What is the average of 2, 5 and 8?

**Answer:** 5.

**10.3.Q3.** Why is boundary handling not an implementation footnote?

**Answer:** It changes the mathematical result at the edges and may create visible or audible artifacts.

**10.3.Q4.** What is the full convolution output length for N=4 and K=3, under this bundle contract?

**Answer:** 4+3-1=6, with zero extension and both sequences nonempty.

**10.3.Q5.** Why test an asymmetric kernel?

**Answer:** Reversing or misaligning a symmetric kernel may accidentally produce the same result and hide a convolution/correlation bug.

**Transfer task:** A symmetric five-tap causal filter runs at 1000 Hz. What is its linear-phase group delay, and what does it exclude?

**Transfer answer:** The delay is (5-1)/2=2 samples, or 2 ms where the response is nonzero. It excludes sensor, scheduling, game update, rendering, and display delays.

**Practical review:** Boundary handling and output alignment change the result. Unity-sum coefficients preserve a constant in steady state, not necessarily at zero-padded finite edges. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_10_3.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

## Lesson 10.4 — Optimization, conditioning and approximation budgets

**10.4.Q1.** Where is the minimum of (x-3)^2?

**Answer:** At x=3, with objective value zero.

**10.4.Q2.** Why can reducing step size help an unstable iteration?

**Answer:** It can prevent updates from overshooting the region where local information is useful, though convergence can become slower.

**10.4.Q3.** What should happen when an iterative method reaches its iteration limit?

**Answer:** Report nonconvergence or the achieved residual explicitly rather than pretending the requested accuracy was met.

**10.4.Q4.** What range of positive alpha makes the scalar quadratic iteration converge from every finite start in exact arithmetic?

**Answer:** 0<alpha<1, because |1-2alpha|<1. Numerical range limitations are a separate implementation concern.

**10.4.Q5.** Why can x=4 be a constrained optimum even though f prime(4)=2 for f=(x-3)^2?

**Answer:** With x>=4, all allowed nearby moves are nonnegative in x and increase the objective. The forbidden move toward 3 is not feasible.

**Transfer task:** For f(x,y)=(x-3)^2+3(y+1)^2, compare alpha=0.1 and alpha=0.4.

**Transfer answer:** At 0.1 the error factors are 0.8 and 0.4, so both decay. At 0.4 they are 0.2 and -1.4; the y error generally grows despite the x error shrinking.

**Practical review:** Reaching the iteration cap or taking tiny steps does not mean convergence. A constrained optimum need not have zero unconstrained gradient, and error terms cannot be combined with unjustified independence assumptions. The full practical work must satisfy the original brief and workbook steps. `labs/reference/lab_10_4.py` exposes the working functions in mathkit.py for inspection; it is not a substitute for your own derivation or tests.

<!-- PAGEBREAK -->
## Module 10 — Written problem solutions

### 10.P01
Find the gradient of f(x,y)=x^2+xy+2y^2 and evaluate it at (1,2).

**Worked answer:** Gradient=(2x+y,x+4y); at (1,2) it is (4,9).

### 10.P02
For F(x,y)=(x+y,x*y), find the Jacobian at (2,3) and its prediction for delta=(0.01,0).

**Worked answer:** J=[[1,1],[3,2]]. J*delta=(0.01,0.03). Here that particular change has no mixed second-order term because y stays fixed.

### 10.P03
Let g(z)=z1^2+z2^2 and F(x,y)=(2x,y). Derive grad(g(F(x,y))) directly and through the Jacobian chain rule.

**Worked answer:** Directly the function is 4x^2+y^2, with gradient (8x,2y). J_F=diag(2,1), grad g at F=(4x,2y), and J_F^T times that vector is (8x,2y).

### 10.P04
Classify the origin for x^2+y^2, -(x^2+y^2), and x^2-y^2.

**Worked answer:** Respectively minimum, maximum, and saddle. All have zero gradient, so first derivatives alone do not distinguish them.

### 10.P05
Find baseband alias magnitudes of 100,700,1100 Hz sampled at 1000 Hz.

**Worked answer:** They are 100,300,100 Hz respectively. These magnitudes alone do not specify the sine phase/sign relation.

### 10.P06
Prove that zero-phase cosines at f and fs-f have identical samples at rate fs.

**Worked answer:** At index n, cos(2*pi*(fs-f)*n/fs)=cos(2*pi*n-2*pi*f*n/fs)=cos(2*pi*f*n/fs). Use integer n and cosine periodicity/evenness.

### 10.P07
A 1,000 Hz sampled signal is reduced by a factor of four. State the new Nyquist boundary and which original content needs suppression before decimation.

**Worked answer:** The new rate is 250 Hz, with boundary 125 Hz. Content above the supported new passband must be attenuated before downsampling, with a practical transition band below/around the boundary as the design requires.

### 10.P08
Compute the unnormalized four-point DFT of [1,1,1,1].

**Worked answer:** X[0]=4; the other bins sum roots of unity to zero, giving [4,0,0,0]. Under the stated convention, the inverse divides by 4.

### 10.P09
Compute full zero-extended convolution of [2,0,1] with [1,2].

**Worked answer:** Outputs are [2,4,1,2], of length 3+2-1=4. Each y[n] sums h[k]*x[n-k].

### 10.P10
Prove convolution by a fixed kernel is linear.

**Worked answer:** For y=(a*x+b*z)*h, distribute the finite sum: sum_k h[k]*(a*x[n-k]+b*z[n-k])=a*(x*h)[n]+b*(z*h)[n]. Use the same extension and alignment policy for all signals.

### 10.P11
A causal three-tap average is applied to a constant finite input of six ones with zero extension. Give the full output.

**Worked answer:** [1/3,2/3,1,1,1,1,2/3,1/3]. Unity gain holds in the full-overlap interior; boundaries reflect the declared zeros outside the input.

### 10.P12
What is the group delay of a symmetric seven-tap causal FIR at 2000 samples/s where its response is nonzero?

**Worked answer:** (7-1)/2=3 samples, or 3/2000 s=1.5 ms. This is not total system latency.

### 10.P13
For f=(x-3)^2, x0=0 and alpha=0.5, compute the next point and gradient.

**Worked answer:** Initial gradient=-6. The update is 0-0.5*(-6)=3, where gradient is zero. This one-step result is specific to the quadratic scaling.

### 10.P14
Prove the scalar quadratic convergence interval for fixed-step gradient descent.

**Worked answer:** With e=x-3, e_next=(1-2alpha)e. Error decays for every starting e precisely when |1-2alpha|<1, equivalent to 0<alpha<1. alpha=1 oscillates, and alpha>1 grows for nonzero initial error.

### 10.P15
Two deterministic absolute error bounds are 0.02 and 0.03 in the same output units. Give a guaranteed combined bound and explain why quadrature is not automatic.

**Worked answer:** The triangle inequality gives at most 0.05. sqrt(0.02^2+0.03^2) is not a general worst-case bound; the two errors may align. Statistical quadrature needs additional assumptions about the errors.

## Module 10 — Review answers

**10.R1.** What changes in a gradient when parameters use different unit scales?

**Answer:** Its numerical components change with those parameterizations. Use a declared scaling/metric and apply chain-rule factors rather than interpreting raw components as universally comparable.

**10.R2.** Why cannot a filter always repair aliasing after sampling?

**Answer:** Different original signals may already produce identical samples, so the missing distinction cannot generally be recovered from those values alone.

**10.R3.** What tests expose an incorrect convolution alignment?

**Answer:** An impulse, an asymmetric kernel, known boundary values, and full output-length checks. A symmetric smoothing example alone can hide reversal errors.

**10.R4.** A solver stops at its iteration cap with a nonzero residual. What should the record say?

**Answer:** Report iteration_limit or nonconvergence plus achieved residual, objective, point, and count. Do not relabel it converged merely because the output is finite.

**10.R5.** What makes Gate B more than a folder of plots?

**Answer:** Written derivations and assumptions, independently checked cases, documented numerical tolerances, raw data and scripts, source/problem logs, error analysis, and a reviewer who can reproduce the central results.
