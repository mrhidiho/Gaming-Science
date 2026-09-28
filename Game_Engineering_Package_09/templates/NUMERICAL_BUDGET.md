# Numerical and quality contract

Operation and useful result:
Representation: bits / signedness / fractional scale / units / dynamic range:
Intermediate widths / operation order / rounding / overflow / saturation:
NaN, infinity, zero, denormal or invalid-value policy where applicable:
Reference/oracle and its independent justification:

## Quality criteria
Bit exact, absolute tolerance, relative tolerance or application-quality metric:
Maximum error / accepted saturation rate / temporal accumulation limits:
Representative distribution and worst cases:
Gameplay threshold or determinism implications:

## Test matrix
Empty/singleton/tail:
Minimum/maximum:
Positive/negative rounding ties:
Near saturation and wrap boundaries:
Accumulated or adversarial sequences:
For every case retain expected output, actual output and acceptance decision.

Mean error alone is insufficient when rare threshold crossings are unacceptable. Record raw-code error and real-unit error separately.
