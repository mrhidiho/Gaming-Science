# Package 05 validation record

Edition: September 28, 2026. Scope: the supplied references, examples, documents and package tools. This record does not certify student submissions or every possible execution.

## Tested environment

Linux x86-64, kernel 6.18.44, glibc 2.41; Python 3.13.5; SQLite runtime 3.46.1; GCC 14.2.0; Clang 17.0.0; CMake 3.31.6. These are observed versions, not claims about the latest available releases. See evidence/environment.json.

## Automated reference checks

| Check | Observed result |
|---|---|
| Native exercise contracts | 62 internal cases passed across eight CTest groups. |
| Native finite-graph integration | 8 internal cases passed in one CTest group. |
| Python exercise contracts | 69 unittest methods passed. |
| Python capstone/integration | 19 unittest methods passed; NATIVE_WORKER set, including all three real-native checks. |
| Combined distinct case count | **158 cases passed**: 70 native plus 88 Python. Parameter loops and repeated configurations are not counted as additional cases. |
| Worked examples | All 20 executed and matched their expected substantive stdout. |
| Finite capstone demo | Real localhost/native/SQLite path; result 29, identical retry response and one retained result row. |
| GCC Debug and Release | Nine native CTest groups passed in each build configuration. |
| Clang ASan + UBSan | Both native test executables built and all nine groups passed, with no reported sanitizer finding in those runs. |
| GCC ThreadSanitizer | Both native test executables built and all nine groups passed, with no reported race finding in those runs. |
| Student scaffolding | Native 16.1 and Python 19.2 checks failed intentionally; unfinished TODO/NotImplemented paths were detected. |
| Release failure gate | A deliberately failing unittest caused nonzero exit and no new release archive. |
| Positive source release | Source-release helper verified the references and created a source archive using the explicitly selected validated build directory. |
| Asynchronous save adapter | Supplemental probes verified snapshot ownership and Future error propagation; these are not added to the 158-case count. |

The sanitizer configurations are separate. Instrumentation was applied to the two native test executables; this is not a claim that every benchmark, subprocess path or Python component was instrumented. No diagnostic result proves absence of all races, undefined behavior, deadlocks or untested defects. Both construction/ownership reasoning and further testing remain required.

## Clean extraction

The release was extracted into a separate directory and the full verifier built native targets in a fresh external build directory, passed all nine native groups and all 88 Python methods, matched all twenty example outputs, and completed the real finite localhost/native/SQLite demo. See evidence/clean_extraction_verification.log. Final additions after that check were validation records, manifests and an interpreter-version clarification in the setup documents, not executable code.

## Document and source audit

The five original module records and all twenty original lesson records match the supplied curriculum JSON. All sixty original quiz questions/answers are preserved; forty application questions are added. Counts were checked for fifty additional problems, twenty-five module-review questions, twelve readiness questions, twenty independent transfer tasks, sixteen code interfaces, four evidence-based labs and ten templates.

Eleven PDFs were generated and rendered with Poppler pdftoppm. All rendered pages were inspected through contact sheets, with selected full-size code/table pages reviewed separately. Text-box checks found no words outside page bounds, and extraction found no replacement-character glyphs. Bookmarks and the lesson/question inventory were checked. These checks are not a formal PDF/UA or comprehensive assistive-technology certification. Final page counts are in source/PDF_COUNTS.json and evidence/content_audit.json.

## Browser review

Chromium 144.0.7559.96 rendered the standalone HTML by content injection. Search, answer expansion, the 9/10 completion threshold plus reading/lab/transfer controls, progress export, valid import, invalid-import rejection without replacing existing state, unique document IDs, and 1440/390-pixel layouts passed the recorded checks. No JavaScript page error was observed.

Direct file:// navigation was blocked by the managed browser with ERR_BLOCKED_BY_ADMINISTRATOR. Actual local-file opening and persistent storage through reload therefore remain **unverified** in this environment. The HTML handles unavailable storage and provides export/import; export before closing or moving it. No browser security policy was disabled to force file access. See evidence/browser_validation.json.

## Measurements, models and untested areas

The four benchmark CSVs contain actual short runs in this shared container: arithmetic, equal-work locality, compact/padded atomic counters and finite-graph worker scaling. The source defines sample counts, warmup, timing boundaries and output checks. These are not device specifications, universal speedup guarantees or sustained thermal/power studies. A cache line of 64 bytes is a labeled hypothetical/layout choice, not a detected target specification. The FCFS scheduler output is synthetic model time, not measured OS scheduling latency.

The RISC-V RV32I/ILP32 routine was accepted by Clang's assembler with the selected target. It was **not executed** on a RISC-V processor or simulator. Host native output does not validate its instruction execution. Host assembly/vectorization reports are included separately.

SQLite was the executed relational backend. The PostgreSQL SQL companion was **not executed**, and SQLite tests do not prove PostgreSQL compatibility. Windows, macOS and Arm-native execution were **not tested**. The supplied command guidance is not a platform-pass claim.

Temporary-save tests use ordinary exception injection and a trusted single-writer scratch directory. They do not simulate real power failure, every filesystem crash mode, hostile path replacement, concurrent truncation or storage-controller behavior. The adapter offloads blocking I/O to a thread; it is not native kernel asynchronous I/O.

ForgeQueue binds only to loopback and executes only a selected trusted native worker. It is not a public authenticated/encrypted service, arbitrary-code sandbox, production availability design, or guarantee of exactly-once computation. It retains request records to constrain durable effects within the stated history scope. Cancellation and timeouts do not imply undoing a completed commit.

## Reproduction

Run `python3 tools/verify.py` from the extracted package root for a fresh reference build. Use the documented native/student and python/student interfaces for independent work. To reproduce a source-release failure gate, select a new archive name and run `python3 tools/make_release.py --output .releases/blocked.zip --inject-failure`; the command should fail and the archive should not exist.

Keep raw logs, investigate disagreements, and narrow claims when an environment blocks a check. Do not convert a missing tool, skipped test or unsupported runtime into a passing result.
