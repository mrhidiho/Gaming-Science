# Trust and failure review

Assets; owner; authorized boundary; actor capabilities; revision: [enter]

## Input and lifecycle contract
Address space, mapping/lifetime, descriptor alignment and length, ownership, generation, reset and completion semantics. Distinguish a local controller model from real DMA.

## Cases
| Case | Expected decision | State permitted to change | Actual result | Evidence |
|---|---|---|---|---|
| Overrun/misalignment/stale owner/etc. | [accept/reject] | [state] | not run | [path] |

## Recovery and limitations
What can an epoch reject? What already-completed or partial operations cannot be undone? State thermal protections, permitted test environment and any external hardware dependencies. No bypass or unauthorized probing is required.
