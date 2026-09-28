# Student contract 12.4: Templates, concepts and data-oriented choices

Write a constrained generic clamp or interpolation function and benchmark two simple entity layouts. Pass: test contracts, record compiler/build mode and explain why the result is workload-specific.

1. Implement a constrained integer clamp and test its accepted types and bound policy.
2. Implement equivalent array-of-structures and structure-of-arrays updates.
3. Collect repeated Release measurements with a verified checksum and saved CSV.
4. Explain the result using only what the workload and measurement support; list one workload that could reverse it.

## Cases

1. below, within and above bounds
2. equal lower and upper bounds
3. reversed bounds rejected
4. same checksum for both layouts
5. zero entities handled
6. multiple sizes and repeated samples recorded

## Evidence

Constrained function, contract tests, benchmark manifest, raw CSV and a bounded interpretation of the measurements.

## Transfer

The hot loop changes from x-only integration to accessing every field of a single selected entity. Predict why the layout conclusion might change, then design a fair test.
