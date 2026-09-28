# Mathematical reference and convention sheet
## Read the conditions with the formula
This is a navigation aid for lessons 06.1-10.4. Derive and test before relying on a formula. Mathematical ^ denotes exponentiation; Python uses **. Angles passed to the supplied trigonometric routines are radians. All numbered examples use the stated model, not a universal engine convention.

## Logic and counting — Module 06
Material implication P -> Q is equivalent to (not P) or Q. It is false only when P is true and Q is false. The converse Q -> P is a different claim. Negating "for every x in D, P(x)" gives "there exists x in D for which not P(x)." A universal claim over an empty domain is vacuously true; an existential claim over an empty domain is false.

Induction needs a base and a preservation step. A loop proof needs initialization, preservation and an exit argument; termination needs a decreasing well-founded measure or another explicit reason. Mathematical proof applies to its model; implementation tests check whether code follows the model.

For n>=0 integers, 1+...+n=n(n+1)/2. Independent sequential choices with counts a,b give a*b combinations. For sets, |A union B|=|A|+|B|-|A intersection B|. A simple undirected graph with n vertices has at most n(n-1)/2 edges. A directed graph without self-loops can have n(n-1).

For positive integer n, repeated floor-halving to at most one takes floor(log2(n)) updates. For n=2^k, T(n)=T(n/2)+1 with T(1)=1 gives 1+log2(n). T(n)=2T(n/2)+n with T(1)=1 gives n(1+log2(n)). State the recurrence and base case before using the result. [R06, R40]

## Vectors and linear systems — Module 07
For Euclidean coordinates, a·b=sum_i a_i*b_i and ||v||=sqrt(v·v). The ordinary normalized vector is v/||v|| only for nonzero v. A zero vector has no unique direction. The projection of v onto nonzero b is ((v·b)/(b·b))*b; the residual is perpendicular to b in exact arithmetic. For unit b, the denominator is one.

Matrix multiplication composes linear maps. With column vectors, applying B first and A second gives A*B*v. A matrix's columns are the transformed basis directions. AB generally differs from BA. A singular matrix loses some input information and cannot have an ordinary inverse. A small numerical pivot may reflect sensitivity or scale; it is not automatically a symbolic singularity proof.

Homogeneous points commonly use w=1; directions use w=0. This bundle uses column vectors and active right-handed rotations. A child maps by M_parent*M_child*p_local. A camera view transform is the inverse of its local-to-world transform. A rigid transform [R,t;0,1] has inverse [R^T,-R^T*t;0,1] when R is orthonormal. Do not transpose a general nonrigid transform and call it an inverse.

A scalar-first unit quaternion is q=(cos(theta/2), axis*sin(theta/2)) for a unit axis. Under the declared rotation action, q and -q represent the same orientation. Normalize accumulated orientations as appropriate; a zero quaternion is invalid. Quaternion multiplication order still matters.

An eigenpair satisfies A*v=lambda*v for nonzero v. Singular values are nonnegative square roots of eigenvalues of A^T*A. Invertible A has two-norm condition number sigma_max/sigma_min. Conditioning is a property of the problem; stability describes an algorithm's response to arithmetic effects.

For an ordinary least-squares line with an intercept and nonconstant predictor: a=sum((x-xmean)*(y-ymean))/sum((x-xmean)^2), b=ymean-a*xmean. Residual r_i=y_i-(a*x_i+b). Derive the objective and assumptions rather than treating this as a universal fitting recipe. [R07, R19, R23]

## Calculus and mechanics — Module 08
Derivative: f'(x)=lim(h->0)(f(x+h)-f(x))/h where the limit exists. The chain rule gives d f(g(t))/dt=f'(g(t))*g'(t). The centered finite difference is (f(x+h)-f(x-h))/(2h); smoothness controls truncation error and floating-point cancellation limits useful h.

For n panels on [a,b], h=(b-a)/n. Left rectangles sum h*f(a+i*h), i=0..n-1. Trapezoids use h*(0.5*f(a)+sum interior f+0.5*f(b)). Signed displacement is the integral of velocity. Total distance integrates absolute speed and need not equal displacement magnitude.

Under constant acceleration a: v(t)=v0+a*t and x(t)=x0+v0*t+0.5*a*t^2. Force has units kg*m/s^2; impulse is integral(force dt) and has units kg*m/s. Mass must be positive for a=F/m.

For a linear spring: x'=v, v'=(-k*x-c*v)/m, m>0. Energy is E=0.5*m*v^2+0.5*k*x^2 and dE/dt=-c*v^2 for this continuous model. With c=0, omega=sqrt(k/m); x(t)=x0*cos(omega*t)+(v0/omega)*sin(omega*t) for omega>0.

Explicit Euler: x_next=x+h*v; v_next=v+h*a_old. Semi-implicit Euler: v_next=v+h*a_old; x_next=x+h*v_next. For the undamped linear oscillator, explicit Euler multiplies energy by 1+omega^2*h^2 each step. The semi-implicit map is in its bounded oscillatory regime for 0<omega*h<2; equality at the boundary is not a safe general prescription. Compare methods at the same final time and inspect energy and trajectory error. [R08, R28; R54 for depth]

## Probability and evidence — Module 09
P(A|B)=P(A intersection B)/P(B), requiring P(B)>0. Independence means P(A intersection B)=P(A)*P(B); do not assume it because trials are repeated. Bayes' detector form is p*s/[p*s+(1-p)*f], with prior p, sensitivity s and false-positive rate f. An impossible conditioning event has an undefined posterior, not automatically zero.

For a finite random variable, E[X]=sum p_i*x_i and Var(X)=E[X^2]-E[X]^2. For a binomial count under n independent equal-probability Bernoulli trials, E[X]=n*p and Var(X)=n*p*(1-p). Expected reward is not a guaranteed one-trial outcome. Seeds support repeatability; unrelated subsystem streams should not interfere through accidental draw ordering.

Sample mean is sum x_i/n. Sample variance uses sum((x_i-xmean)^2)/(n-1), n>=2. Under independent identically distributed sampling, estimated standard error is s/sqrt(n). Under the appropriate independent normal model, a Student-t interval for the mean uses xmean +/- tcritical*s/sqrt(n). For paired comparisons, analyze the paired differences, not two unrelated sets of samples. The statistical assumptions are not established by computing the formula.

This bundle's empirical percentile convention is nearest rank: sorted[ceil(p*n)-1] for 0<p<=1; p=0 is the minimum. At small n, p95 can miss a single worst observation. Always report count, method, raw data and at least an appropriate extreme/tail check.

RMSE=sqrt(mean((actual-predicted)^2)). Separate fit and evaluation data. Correlation is not a causal conclusion; adjacent times may be dependent. Synthetic data must not be labeled as collected player telemetry. [R09, R06]

## Gradients, signals and optimization — Module 10
For scalar f of several coordinates, grad f collects partial derivatives. For vector-valued F, J_ij=partial F_i/partial x_j. Small changes satisfy deltaF approximately J*deltaX. With column gradients, grad(g composed with F)=J_F^T*grad g. A zero gradient may be a minimum, maximum, saddle or another stationary point.

The sampling rate fs has units samples/second; the Nyquist boundary is fs/2 Hz. Unique reconstruction of a strictly band-limited signal requires appropriate assumptions and a rate above twice its highest frequency. Practical filters need transition bands. For real sinusoids the alias magnitude can be computed by r=f modulo fs, then min(r,fs-r); phase/sign must still be tracked. Post-filtering cannot generally undo already-overlapped aliases.

The unnormalized N-point DFT is X[k]=sum_(n=0..N-1) x[n]*exp(-j*2*pi*k*n/N). Here j^2=-1 and exp(j*theta)=cos(theta)+j*sin(theta). This describes frequency coordinates of the finite sample sequence, not an automatic claim about a unique continuous signal.

Full zero-extended convolution is y[n]=sum_k h[k]*x[n-k]. For nonempty lengths N,K the output length is N+K-1. A causal symmetric K-tap FIR has linear-phase group delay (K-1)/2 samples where its frequency response is nonzero; divide by fs for seconds. Boundary extension and output alignment change edge results.

For f(x)=(x-3)^2, gradient descent is x_next=x-2*alpha*(x-3). Error e_next=(1-2*alpha)*e, so fixed-step convergence for all finite initial errors in exact arithmetic requires 0<alpha<1. alpha=1 oscillates unless already at the minimum; alpha>1 diverges for a nonzero error. A finite step budget is a resource limit, not proof of convergence.

Deterministic absolute error bounds in the same output units can be added by the triangle inequality. Root-sum-square is not a universal substitute: it needs justified error statistics and dependence assumptions. [R10, R41, R42]
