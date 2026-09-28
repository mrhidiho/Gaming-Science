# Volume 10 code laboratory

Run commands from the extracted package root unless a section explicitly says otherwise. The core reference models and tests use Python’s standard library. Python 3.13.5 on Linux x86-64 was used for the packaged validation; the code’s language baseline is Python 3.10+. Other interpreters and operating systems were not executed here. `python3` may be the command name on your machine.

## Core reference route

```sh
python code/check_environment.py
python code/run_tests.py
python code/demo.py --out my_evidence/reference_outputs
```

The reference suite contains 83 test methods. Exhaustive subcases include 46,656 length-six atomic coherence traces and the SECDED campaign’s 16 clean, 128 single-bit and 448 double-bit cases. They are subcases, not 46,000 separately named unit tests. All of those claims apply to the bounded models and tested implementation.

The demo produces thirteen deterministic files. It exercises three equal-capacity cache geometries over three synthetic traces, a miss-penalty sensitivity sweep, coherence and scheduler traces, analytical timing/PPA examples, an ECC campaign, a CDC mailbox, finite queue exploration, paired synthetic analysis and a local descriptor/reset model. Read each file’s scope labels. These are not real game benchmarks, silicon measurements or completed thesis results.

## Student route

Implement the eight functions in `code/student/exercises.py`. Read `code/EXERCISES.md` and inspect `code/tests/test_exercises.py` before starting.

```sh
python code/run_tests.py --student
```

This route fails until implemented. The default reference suite does not accidentally run unfinished student code. Add new adversarial tests rather than weakening the provided contracts. After a first attempt, compare the reference methods in `code/reference/`. Finishing eight functions does not complete all twenty labs.

## C++ publication route

A C++17 compiler, CMake and a thread implementation are needed. The recorded environment used GCC 14.2.0 and CMake 3.31.6. The following commands were exercised with equivalent package/build paths:

```sh
cmake -S code/cpp -B my_evidence/cpp-build -DCMAKE_BUILD_TYPE=Release
cmake --build my_evidence/cpp-build
ctest --test-dir my_evidence/cpp-build --output-on-failure
```

There are three CTest checks: safe one-shot publication, rejection of zero rounds and rejection of invalid text. Main writes the non-atomic payload once, publishes the atomic flag with release, and never changes the payload before the consumer finishes. The consumer waits with acquire and reads the payload only after it observes publication. Passing a finite test is not a universal proof; annotate the happens-before argument in Lab 46.1.

## Optional RTL, formal and physical flow

Read `code/rtl/README.md` first. The package supplies a four-entry synchronous FIFO, scoreboard testbench, initial occupancy/accounting properties, SBY configuration, educational timing constraints and an ORFS config example. The package validation did **not** execute Icarus Verilog, Yosys/SBY/SMT or OpenROAD. They were unavailable in the build environment. No HDL simulation pass, formal proof, DRC/LVS pass or physical PPA result is claimed.

Pin and install an authorized toolchain independently, review the source and run the required routes. Complete the additional payload-order properties, cover/mutation evidence and stage reports before claiming the corresponding lab or project is done. The sample SDC is a teaching contract to adapt and review, not universal signoff constraints.

## Model boundaries

`coherence.py` has atomic transitions, not asynchronous message races. `scheduler.py` models a fixed-latency dependency graph, not an ISA, branch predictor or complete CPU. `cache.py` is cold read-only modulo-indexed LRU with a serial cost model. `models.py` computes explicitly stated arithmetic, not characterized physical results. `protocol.py` uses ideal digital edges and coordinated reset, not analog metastability. `ecc.py` covers the stated extended Hamming code and fault classes. `security.py` manipulates local Python state and never accesses a device. `analysis.py` demonstrates paired resampling; experimental independence must be established by the study design.

## Evidence and release integrity

`validation/` records the actually executed checks. `examples/` is the unmodified reference-output directory. Create your own outputs outside it. `VALIDATE_PACKAGE.py` checks the release’s inventoried files and lesson counts without altering files or using the network. After editing an inventoried source, a hash mismatch is expected; it identifies a changed release, not automatically a bug.
