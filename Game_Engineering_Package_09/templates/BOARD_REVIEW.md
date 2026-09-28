# Schematic and board review — no fabrication authorization

Design purpose and exact low-speed peripheral:
KiCad version / project path / schematic revision / layout revision:

## Checks requiring evidence
| Item | Evidence path / exact datasheet section | Finding and resolution |
|---|---|---|
| Supply and voltage-domain compatibility | | |
| Steady and transient power/current budget | | |
| Pin and connector orientation | | |
| Footprint pin numbering and mechanical fit | | |
| Decoupling intent and return paths | | |
| Clock, reset and startup state | | |
| ERC findings | | |
| DRC findings | | |
| Probe access and staged bring-up observations | | |

The course's JSON board linter checks a small declaration only. Include actual KiCad schematic/layout files and their review findings for the original assignment. A visually clean board or zero DRC errors does not prove electrical correctness.

## Optional physical extension
Exact approved power source, operating limits, instrumentation, supervision and stop conditions:
Qualified reviewer / scope of review / unresolved concerns / disposition:
Do not power or fabricate a design based only on this checklist or a simulation pass.
