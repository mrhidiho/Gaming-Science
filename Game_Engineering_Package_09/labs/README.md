# Runnable computational slices

There is one `solve(case: dict) -> dict` starter and reference module for each lesson 36.1–40.4. The starter docstring declares the case fields, units and simplifications. The reference includes validation and an implementation. Demos execute representative inputs; JSON cases contain independent expected results and required exception classes.

From the package root:
```text
python -m labs.run list
python -m labs.run demo 37.2
python -m labs.run check 37.2 --student
python -m labs.run all
python -m unittest discover -s labs/tests -v
```
The default checker uses reference implementations. Add --student for your work. Unimplemented starters intentionally raise NotImplementedError. Published cases are not exhaustive, so add tests for the full declared contract and original practical requirements. Invalid-field type validation is bounded to the documented input shape; these educational helpers are not hardened parsers for untrusted production services.

See LAB_WORKBOOK for the original assignments. The scheduler omits real interrupt/blocking overhead; the board linter is not KiCad; the GPU examples are abstract models; the trace has no photons; the XR slice is numerical; the descriptor model performs no DMA. These limitations are part of the exercise, not optional disclaimers.
