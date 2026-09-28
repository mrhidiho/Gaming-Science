# Student contract 12.1: RAII and resource ownership

Wrap a mock file/device resource whose open/close counters can be inspected. Inject failure after acquisition. Pass: each acquired resource is released exactly once and no view outlives its owner.

1. Implement or inspect a mock resource with observable acquisition and release counters.
2. Wrap it in a non-copying RAII owner and test normal completion, early return and injected failure.
3. Add an enclosing object with dependent members and explain partial-construction cleanup.
4. Draw the device-before-resource construction and resource-before-device destruction order.

## Cases

1. successful scope releases exactly once
2. injected exception releases exactly once
3. empty owner releases nothing
4. nested owners unwind in reverse order
5. all paths return live count to baseline

## Evidence

Acquisition/release ledger, fault-injection tests, ownership diagram and destruction-order explanation.

## Transfer

A file close operation can fail when flushing buffered data. Separate explicit error-reporting close from destructor cleanup without allowing two releases.
