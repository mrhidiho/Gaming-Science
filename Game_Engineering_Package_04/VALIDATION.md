# Package 04 validation

## Executed code checks

The final reference source was built and tested on Linux x86-64 using GCC 14.2.0 in Debug and Release, and Clang 17.0.0 in Debug with AddressSanitizer and UndefinedBehaviorSanitizer. CMake 3.31.6 and Ninja 1.12.1 were used. Each of the three configurations passed all **24 CTest reference programs**: 20 lesson programs and four actual-C/C++ bridge programs. Warnings were enabled and treated as errors. The C17 source explicitly rejects C++ compilation.

These are 24 test programs per configuration, not 72 independent specifications. A program may evaluate many repeated assertions during randomized/differential checks. The raw check counts are recorded without presenting them as that many unique test cases.

The twenty student starters also compile with the configured warning policy. All twenty initially fail with a TODO message; that is intentional. Their initial checks are only part of the workbook's full acceptance contract. Running a reference executable or changing the starter's expected values is not completed student work.

The six-command C++ grid trace was compared byte-for-byte with an independent Python implementation and the checked-in golden CSV. The build-stage helper first successfully compiled a valid source, then confirmed the intended syntax and missing-definition rejections. No deliberately invalid lifetime example was executed.

The Release layout benchmark completed with matching checksums for both layouts and emitted sixteen raw timing samples. Those samples concern this execution environment and a narrow x/vx update, not the learner's hardware or a general engine-layout recommendation.

## Evidence files

- validation/environment.json — compiler, platform and build configuration record.
- validation/test_debug.log, test_release.log, test_sanitize.log — final CTest transcripts.
- validation/reference_checks.txt — per-program output and repeated check counts.
- validation/test_starter.log — expected initial student failures.
- validation/replay_comparison.txt — native/Python/golden replay match.
- validation/diagnostics.log — controlled compile and link experiments.
- validation/layout_sample.csv — actual benchmark samples, not illustrative fabricated measurements.
- validation/reader_tests.txt — browser interaction checks and their limitations.
- validation/content_checks.json — canonical lesson/quiz continuity and PDF checks.

## Browser and document checks

The HTML reader's search, zero-match behavior, score/progress controls, export, valid/invalid import, answer disclosure and unavailable-storage fallback were exercised in Chromium with in-memory HTML rendering. Desktop and mobile layouts were rendered; mobile page width was checked for overflow. Managed test-browser policy blocked direct file and loopback navigation, so persistent local-file browser storage across reloads was **not** verified. The reader catches storage failures and provides JSON export/import. No external script, stylesheet, font or image asset is needed to display the course.

The PDFs were rendered for visual inspection of covers, body pages, code, tables and references. Automated checks scan all pages for text outside page bounds and missing/replacement glyphs, and record actual page counts. Sampled layout inspection is not a claim that every page was independently typeset by hand. The original quiz data is compared exactly to the retrieved original curriculum, while added questions remain separately identified in the source JSON.

## Limits of the evidence

Windows, macOS, other toolchain versions, physical devices and proprietary game SDKs were not executed. The examples are narrow educational implementations, not production engines, generic standard-container replacements or a hostile-code security sandbox. Sanitizers cover executed paths and do not prove all-input correctness. Generated expressions, randomized container operations and small-graph oracles increase evidence but do not replace proofs of stated invariants and assumptions.

The parser/compiler/tree evaluator accept only parser-produced owned ASTs under the documented limits. The ring buffer and C mock failure hooks are single-threaded. The educational int buffer and map disable copy/move rather than expose invalid moved-from metadata. Source edits change the original manifest hashes by design; preserve the ZIP as a reference and record your own changes.

## Reproduce the core checks

From the extracted package root:

```sh
cmake -S code -B build/debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build/debug --config Debug --parallel 2
ctest --test-dir build/debug -C Debug -L reference --output-on-failure
```

Use a fresh directory for Release or sanitizer configurations; follow START_NEXT.pdf. The optional manifest helper checks the unedited shipped files:

```sh
python3 code/tools/verify_manifest.py
```

Hashes provide integrity checking against this manifest, not a cryptographic publisher signature. Added local build products are not part of the shipped inventory.
