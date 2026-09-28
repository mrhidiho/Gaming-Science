# Hardware lab record

Requirement and evidence tier: behavioral simulation / synthesis estimate / routed model / measured board.

## Safety before power
Use simulation first. For physical work: supervised low-voltage equipment, current limit, power-off wiring, ESD precautions and an inspected connection plan. No mains, opened power supplies or improvised lithium-battery work.

## Interfaces and assumptions
Clock/reset, voltages, pin constraints, timing, protocol, endianness, alignment, ownership and failure behavior.

## Verification
Reference model, directed/random tests, assertions, coverage, CDC/reset review, negative tests and unresolved properties.

## Tools and constraints
Exact tool/library/ISA versions; clock and I/O constraints; implementation stage.

## Evidence
Simulation traces, synthesis/timing/area reports or calibrated measurements. Keep these categories distinct.

## Limitations
Unmodeled electrical, physical, manufacturing, reliability or security effects. No commercial silicon signoff is implied.
