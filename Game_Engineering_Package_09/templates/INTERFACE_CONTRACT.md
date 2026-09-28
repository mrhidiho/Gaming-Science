# Interface contract

Project / revision / author / reviewer / date:

## Useful operation
Inputs, outputs, units, numerical format, byte order, exceptional values and oracle:

## Electrical and transport boundary
Exact device/board documentation and revision (for optional physical extension):
Voltage domains, directions, pin/connector views, current/power limits, loading and return paths:
Transport role, mode, bit order, framing, transfer maximum, timeout origin and deadline equality policy:
What the simulator knows that the real transport cannot automatically diagnose:

## Descriptor and lifetime
Registered buffer(s), element stride, byte offset, count, alignment and overflow-safe bounds check:
Operation/format validation, context/permissions, request ID and epoch:
Ownership states; allowed readers/writers in each state; completion boundary; reuse event:
Timeout, duplicate/stale completion, cancellation, acknowledged quiescence, reset and removal:

## Acceptance tests
Normal / empty / singleton / tail / malformed / stale / timed out / reset / wrong context:
For each: input, expected transition/output, actual artifact and remaining limitation.

## Review decision
Unresolved requirements and reviewer findings:
Physical fabrication or bring-up authorization, if any, must come from a qualified review of the exact implementation. This template and simulation results are not authorization.
