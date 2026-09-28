# Package validation report

Package 10 / Volume 9 — Graduate Game-Engine and Graphics Engineering

Edition: September 28, 2026. This report covers the delivered reference artifact, not learner assessment or an independent reproduction of a research result.

## Content integrity

The five original module records, 20 lesson IDs/titles/outcomes/primers/examples/labs/readings, and all 60 original quiz questions and answers were compared against the recovered Volume 9 source. Original fields are unchanged inside the expanded JSON. There are 20 expanded lab procedures, 40 graduate problems with 40 solutions, and 20 deliberately unfinished learner warm-ups. Reading IDs resolve; browser anchor IDs are unique and internal links resolve. See `content_checks.json`.

## Executed code validation

The Python reference suite passed **64 tests** in both ordinary and optimized (`-O`) execution. The optimized run checks that essential correctness is not accidentally disabled with assertions. Tests include solver residual/known-solution behavior, exact scan and compaction, tiling/pipeline model cases, MIS and reservoir primitives, BVH comparison with brute traversal, finite-depth emitter support, XPBD/dense-oracle agreement, bounded resource/state cases and compiler semantics. See `python_tests.txt` and `python_optimized_tests.txt`.

The C++20 reference passed CTest in GCC Debug, GCC Release, and Clang Debug with AddressSanitizer plus UndefinedBehaviorSanitizer. Each executable checks 12 scan sizes including empty/partial/non-power-of-two boundaries, 100,000 u32 expression-equivalence cases, and a loop-carried-dependence example. Checks remain active in Release. See the three `native_*.txt` build/test logs. Sanitizers did not report a failure in these runs; this is not proof of all-input memory safety.

All six experiment groups ran and their outputs are in `evidence/reference_run`: numerical, parallel models, linear bar, rendering, system models and compiler. A separate native CPU benchmark recorded 12 within-process paired trials; those are not 12 independent experiments. Read `evidence/README.md` before interpreting any numbers. The CPU path tracer's depth convention permits an emitter hit after the final allowed scattering vertex, keeping the truncated NEE/BSDF path support aligned; dedicated tests cover that boundary.

The learner warm-up checker reports **20 pending, zero passing and zero failed** on the untouched starters and returns expected exit code 2. This is intentional unfinished learner work, not a reference failure. See `learner_starter_status.txt`.

## Documents and browser

All 11 PDFs were generated and rendered. Automated checks found no extracted text outside page bounds, missing replacement glyphs, invalid bookmark destinations or split three-question quiz blocks. Representative covers, body pages, table/contents pages and contact sheets were visually inspected; the grading table's column widths and quiz pagination were corrected during review. PDF page counts are in `pdf_page_counts.json`.

The browser JavaScript passed Node syntax checking. Isolated Chromium rendering/interaction tests checked 20 lesson panels, initially closed answers, filtering, in-session progress, unavailable-storage handling, export-Blob contents, compatible import, rejection of invalid lesson IDs, and a 390-pixel layout without document-level horizontal overflow. No uncaught JavaScript errors or external HTTP(S) requests occurred in those tests.

Browser limitation: managed Chromium policy blocked both file-URL and localhost navigation in this environment. UI tests therefore injected the already-generated HTML into an opaque `about:blank` document without changing that policy. Native local-file launch, native storage persistence across reload, and actual saved browser downloads were **not validated**. These limits are explicit in `browser_tests.json`; they are not recorded as passes. The course is self-contained and includes progress export/import and a storage-unavailable fallback. PDFs remain available independently of browser behavior.

## Not validated or not implemented as production features

No CUDA compiler/device execution was available. `code/gpu/reduction.cu` was not compiled, executed, sanitized or benchmarked; all device-specific checks remain pending. Python models and native CPU tests are not substitutes for GPU validation.

The bar is a one-dimensional linear model, not full 3D cloth. The weighted reservoir is not a complete ReSTIR implementation. The scalar inverse fit is not a trained neural renderer. The bounded store assumes an atomic persistent sink; it is not replicated consensus or real crash durability. The finite lifecycle model checks safety for its stated bounds, not liveness. The restricted DSL is not an operating-system sandbox or executable native JIT. Larger domain-specific projects and Gate I independent review remain learner assignments.

Only the recorded Linux x86_64 environment was used for native/reference execution. Other Python versions, operating systems, compilers and GPU targets remain unverified. Passing these tests supports the named checks only; it does not certify general performance, production readiness or learner completion.

## Recorded toolchain

```text
Python: 3.13.5 (main, Jul 15 2026, 20:25:40) [GCC 14.2.0]
Platform: Linux-6.18.44-x86_64-with-glibc2.41
C++: g++ (Debian 14.2.0-19) 14.2.0
Clang: clang version 17.0.0 (https://github.com/swiftlang/llvm-project.git 10999b6d034fe318f3d56c83bddb6572593a8bb0)
CMake: cmake version 3.31.6
Node: v22.16.0
```

## Integrity files

`FILE_MANIFEST.json` inventories payload files and hashes, excluding itself and the checksum file to avoid a self-referential digest. `SHA256SUMS.txt` covers every other packaged file, including the file manifest. The ZIP is separately CRC-tested after creation, and its file entries are checked against that inventory. These checks detect changed bytes; they do not replace semantic review.
