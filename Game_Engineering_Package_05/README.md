# Package 05 · Expanded Volume 04
## Computer Systems and Software Engineering

Begin with START_NEXT.pdf or source/START_NEXT.md. This is Modules 16–20, lessons 16.1–20.4, Gate D, following the existing C++/algorithm/language prerequisites. It is not Volume 5 (graphics).

## Included

Twenty expanded lessons and twenty runnable examples; sixteen student/reference coding interfaces; four evidence-based engineering labs; 100 lesson quiz questions (60 retained and 40 new); 50 additional problems; 25 module reviews; twelve readiness questions; five integration projects; and the Gate D specification with a worked local service. Student files are intentionally unfinished.

The main PDFs are START_NEXT, STUDENT_HANDBOOK, LAB_WORKBOOK, ANSWER_KEY, CAPSTONE_SPEC and SYSTEMS_REFERENCE. Five module PDFs are in modules. COURSE.html is the self-contained searchable browser edition with self-recorded progress. Markdown and structured JSON are in source. External readings are linked, not copied books.

## Build and run

From this directory, with a C++20 compiler, CMake and Python 3.10 or newer already available:

```sh
python3 environment_check.py
cmake -S native -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --config Debug --parallel 2
ctest --test-dir build -C Debug --output-on-failure
python3 tools/run_example.py 16.1 --build-dir build
python3 check_lab.py 16.1 --student
```

On Windows use the verified Python launcher (often `py -3`) instead of `python3`. The example runner locates common single- and multi-configuration executable paths. Native executable files are compiled locally, not shipped as platform-specific binaries.

A student check failing with TODO/NotImplemented is expected until implemented. `--reference` checks worked code, not student competence. The full reference verification creates a fresh build, runs tests and examples, and performs an actual finite localhost exchange:

```sh
python3 tools/verify.py
```

To run the finite capstone demo after building, use the native executable path in your build directory (on a multi-config generator it may be `build/Debug/native_worker.exe`):

```sh
python3 capstone/reference/run_demo.py --native build/native_worker
```

A verified source-only release can be made with:

```sh
python3 tools/make_release.py --output ForgeQueue_Source.zip
```

The release command refuses to overwrite an existing archive and runs verification before creating output. The source-only release includes editable documentation instead of the large PDFs/browser edition.

## Layout

- native: C++20 examples, references, unfinished student headers, contract/graph tests, benchmarks, trusted worker and separate RISC-V assembly.
- python: OS/protocol/SQLite exercises, examples and tests.
- capstone: worked service/gateway and unfinished student integration scaffold.
- sql: optional PostgreSQL comparison exercise; not an executed compatibility claim.
- tools: example runner, full verifier, query-plan experiment and source-release helper.
- data: deterministic expected worked-example outputs.
- evidence: actual validation/benchmark observations and environment information.
- templates: ten blank evidence/review records.
- source: editable teaching material, untouched curriculum slice, expanded JSON and references.

## Boundaries

No root privileges, system tuning, GPU, cloud account or public listener is needed. Only synthetic inputs, private scratch files and loopback sockets are used. Do not configure arbitrary untrusted executables as the native worker. SQLite is the executed database backend; the PostgreSQL companion is optional and explicitly not executed here.

Source reproduction does not imply bit-identical binaries across toolchains. Reference tests do not prove all interleavings, hostile-input security, power-loss durability or student understanding. Consult VALIDATION.md for exact checks, environment and limitations; SOURCES.md distinguishes the original material from expansion references.
