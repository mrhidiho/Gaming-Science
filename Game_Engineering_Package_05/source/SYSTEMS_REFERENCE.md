# Systems reference
## Commands, contracts and debugging questions

## Build and test

Run from the package root with an installed C++20 toolchain. On Windows replace `python3` with the verified Python launcher, such as `py -3`.

```sh
cmake -S native -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --config Debug --parallel 2
ctest --test-dir build -C Debug --output-on-failure
python3 tools/verify.py --build-dir build
```

A multi-configuration generator may place executables below `build/Debug`. The example runner locates that layout:

```sh
python3 tools/run_example.py 18.2 --build-dir build
python3 check_lab.py 18.2 --student
python3 check_lab.py 19.4 --reference
```

`verify.py` always tests the worked references. It does not assess the unfinished student implementation. Omitting its build directory creates a fresh build under `.build`.

## Optimized experiments

```sh
cmake -S native -B build-release -DCMAKE_BUILD_TYPE=Release
cmake --build build-release --config Release --parallel 2
```

Run the applicable executable in that build: `benchmark`, `locality_benchmark`, `false_sharing`, or `graph_benchmark`. Redirect standard output to a new CSV file. Do not overwrite earlier trials without preserving them. For a multi-configuration Windows build the files commonly end in `.exe` under `build-release/Release`.

| Experiment | Included work and cautions |
|---|---|
| benchmark | Separate compiled arithmetic kernels, checksum validation, warmup and varied order. Inspect whether optimization makes both variants similar. |
| locality_benchmark | Equal useful element count, generated index paths, index reads included. It is not a direct DRAM-latency meter. |
| false_sharing | Two atomic writers plus thread startup/join. 64-byte alignment is a chosen layout, not discovered hardware. |
| graph_benchmark | Finite graph execution, worker creation and aggregation. A simple ready-scan reference, not work stealing. |

All performance conclusions are workload- and environment-specific. Zero improvement is a valid result. Separate Debug, Release and sanitizer data.

## Host assembly and vectorization reports

GCC example, run in a scratch output directory:

```sh
g++ -std=c++20 -O3 -S -fopt-info-vec-all=vectorization.txt \
    native/kernels.cpp -o kernels.s
```

Clang alternative:

```sh
clang++ -std=c++20 -O3 -S -Rpass=loop-vectorize \
    -Rpass-missed=loop-vectorize native/kernels.cpp -o kernels.s
```

These commands produce assembly for the compiler's configured host/target. They do not turn x86-64 output into RISC-V output. `native/asm/sum_u32_rv32.S` is a separately authored RV32I/ILP32 teaching routine. In package validation it was accepted by Clang's RISC-V assembler; it was not executed on a RISC-V target. [P01–P03, P16]

## Separate sanitizer builds

```sh
cmake -S native -B build-asan -DCMAKE_BUILD_TYPE=Debug \
    -DSANITIZER=address
cmake --build build-asan --config Debug --parallel 2
ctest --test-dir build-asan -C Debug --output-on-failure

cmake -S native -B build-tsan -DCMAKE_BUILD_TYPE=Debug \
    -DSANITIZER=thread
cmake --build build-tsan --config Debug --parallel 2
ctest --test-dir build-tsan -C Debug --output-on-failure
```

The address option combines AddressSanitizer and UndefinedBehaviorSanitizer in the supplied GCC/Clang configuration. ThreadSanitizer is a separate build; do not combine it with AddressSanitizer. Platform/runtime support varies. Record unsupported or failed instrumentation honestly. No diagnostic report is a proof of all schedules, lifetimes or progress. Never change system security settings merely to force a sanitizer to start. [P04, P05]

## Architecture arithmetic

| Quantity | Definition under a stated model |
|---|---|
| Frame interval | `1000 / frames_per_second` milliseconds. A target interval is not a measured guarantee. |
| Cache memory block | `floor(byte_address / line_bytes)`. |
| Direct-mapped index | `block mod line_count`. |
| Direct-mapped tag | `floor(block / line_count)`. Validity still matters. |
| Virtual page / offset | `address // page_bytes`, `address % page_bytes`. No physical frame is inferred. |
| Complete vector blocks | `n // width`; tail is `n % width`. |
| Ideal Amdahl speedup | `1 / (serial_fraction + (1-serial_fraction)/workers)`. |
| Graph lower bound | At least `max(total_work/workers, critical_path)` under ideal assumptions. |

Latency is delay for a result; throughput is completed useful work per unit time. Neither is just clock frequency. Data-cache misses, translation misses and page faults describe different events.

## Concurrency contracts

A synchronization argument should name every shared location, its owner, all conflicting accesses, the required invariant, the ordering primitive and the destruction point. A data-race-free program can still have a logical race or deadlock.

One-shot publication:

```text
producer payload write
    -> release store to ready
    -> acquire load observing that publication
    -> consumer payload read
```

Assumptions: one publication, no later payload mutation, correct flag identity and live storage. `volatile` is not a substitute.

Bounded queue predicates:

```text
producer may progress: closed OR size < capacity
consumer may progress: closed OR size > 0
```

Change state under the agreed mutex. Recheck predicates after waking. Notify both groups on closure. Stop admission and join only after releasing resources workers need. Discarding queued work does not revoke an already popped job or undo a committed result.

## Framing and request validation

```text
4 bytes: unsigned big-endian body length
N bytes: body, where 1 <= N <= 4096
```

TCP does not preserve application messages. Test fragmentation, coalescing, EOF, zero/oversized length, byte budget and absolute deadline. The parser's explicit chunk limit is different from the gateway's one-request-per-connection policy.

The version-1 schema accepts only `version`, `id`, `operation` and `values`. Check exact types, including exclusion of boolean values from integer fields. Validate before allocation or execution. A timeout means missing observed progress, not proof that a remote effect never happened. [R17, P09]

## Persistence and databases

The save example's replacement boundary decides whether the old or new file is visible under ordinary exception injection. Its file fsync does not by itself prove directory/name or device-level power-loss durability. Temporary-file cleanup is not transaction rollback after replacement. [P06]

A database transaction and a connection lifetime are different. The SQLite exercises use explicit transactions, enable foreign keys per connection, and close connections deliberately. The reference does not share one SQLite connection among workers. Use parameters for values, not string concatenation. Compare actual plans with `python3 tools/query_plan.py`. [P10–P12]

For deduplication, commit the intended effect and its identity/payload/result record together. Preserve the record for the stated retry scope; same ID with different work is a conflict. A transaction in one database does not include another service automatically.

## Troubleshooting without destructive fixes

| Symptom | First checks |
|---|---|
| Compiler cannot build jthread/span | Confirm compiler and standard-library support, selected C++20 mode and the Volume 3 setup. |
| Native example not found | Build the target and use run_example.py with the correct build directory/configuration. |
| Student test raises TODO | Expected until that exercise is implemented. Do not switch to reference and call the student complete. |
| Import fails | Run documented commands from the extracted package root; keep package directories together. |
| sqlite3 module missing | Use an approved Python installation that includes that standard-library extension; do not install a random similarly named package. |
| Socket test is blocked | Confirm the environment permits local loopback sockets; record the limitation. Do not expose a public port. |
| Shutdown hangs | Inspect every wait predicate, notification path, lock held during join and job termination assumption. |
| Save reports failure but changed | Check whether the failure occurred after replacement/commit. Do not infer rollback from an exception. |
| Benchmark shows no speedup | Verify equal results and intended executed code, then inspect overhead, working set and trial variability. |
| Sanitizer cannot initialize | Keep the log and report unsupported runtime conditions; do not claim a clean diagnostic pass. |

## Releases and evidence labels

```sh
python3 tools/make_release.py --output .releases/forge-source-v1.zip
python3 tools/make_release.py --output .releases/must-not-exist.zip \
    --inject-failure
```

The second command intentionally fails before creating a new archive. Use a new output filename. The main course ZIP has its own manifest and contains the documents; the source-release helper packages a smaller code-focused handoff plus its manifest.

Use these labels in reports: **hand-derived model**, **measured on stated system**, **automated checks passed**, **reviewed argument under assumptions**, **not tested**, or **blocked by environment**. Do not merge them into a single unqualified claim that the system is proven correct.
