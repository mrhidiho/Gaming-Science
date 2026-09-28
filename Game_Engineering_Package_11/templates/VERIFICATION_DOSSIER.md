# Verification dossier

DUT / revision / interface contract: [enter]

## Property matrix
| Property | Assumptions | Configuration | Method | Cover/mutation | Outcome | Evidence |
|---|---|---|---|---|---|---|
| [property] | [restriction] | [parameters] | [proof/bounded/simulation] | [case] | not run | [path] |

## Assumption review
Can inputs create accepted traffic? Are reset and clocks constrained more than the real environment? Which guarantee belongs to another component? How is an assume-guarantee interface checked at integration?

## Counterexamples and mutations
Retain original failing trace, explanation, repair and rerun. A timeout is inconclusive, not PASS.

## Residual scope
List data ordering, liveness, CDC/analog, faults, physical timing and trust properties not covered. Explain why the dossier does or does not support each thesis claim.
