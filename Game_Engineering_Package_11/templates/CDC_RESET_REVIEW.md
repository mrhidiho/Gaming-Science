# CDC and reset review

Source/destination domains; clock assumptions; payload width; throughput; protocol; revision: [enter]

## Transfer contract
When is a source item accepted? How long is data held? When is it delivered and acknowledged? How are backpressure and stopped clocks handled?

## Reset epochs
Define coordinated reset/flush behavior and the fate of accepted but undelivered data. State whether unilateral reset is allowed. If allowed, provide the recovery protocol and evidence, not an assumption that both domains are empty.

## Evidence
Record phase/ratio tests, coincident-edge semantics, assertions and covers, accepted/delivered sequence comparison, full/busy behavior and reset cases.

## Analog boundary
State synchronizer implementation and vendor/tool review needs. Do not compute or claim MTBF from the digital Python trace. List metastability, skew and placement concerns not discharged by simulation.
