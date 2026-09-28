# Validation summary — September 28, 2026

## Executed and passed

- 123 Python contract tests across 20 reference exercises, including 3 state/history checks.
- 20 Python cooker/BVH integration and malformed-input tests.
- 200 C++ assertions in one CTest test executable; repeated with AddressSanitizer and UndefinedBehaviorSanitizer.
- All 20 reference demonstration expressions.
- Deliberately incomplete Lesson 21.1 starter failed with NotImplementedError, as expected; the starter track does not fall back to reference code.
- Asset cook, content digest checks, fresh-directory deterministic output, dependency invalidation, malformed-source manifest preservation and C++ cooked-mesh rendering.
- Seeded 256-sphere/1,000-ray BVH comparison matched the brute-force hit oracle; raw timings and counters are in evidence/.
- Node syntax check for the WebGPU JavaScript.
- Automated clean-folder validation with a path containing spaces: tests, build, cooker, BVH and three render commands passed. This was NOT an independent human review.
- Static browser-edition check: 20 lesson cards, 20 answer disclosures, 100 questions, all local links resolve.
- PDF page/word geometry checks show no off-page text. Handbook, workbook and reference sheets were rasterized with Poppler; contact-sheet inspection was used to repair sparse spill pages and check layout. PDFs contain navigation bookmarks; the handbook has a linked contents page.

## Not executed / not claimed

- WebGPU device execution, WGSL compilation, native GPU backend validation, GPU timing, device-loss recovery or physical-driver stress tests.
- Windows/macOS execution or cross-platform bitwise identity.
- The complete learner engine, asynchronous runtime residency, live editor, full PBR/temporal methods or the integrated Gate E failure matrix.
- The required second-person clean-build and oral review.
- Browser UI automation: attempted headless Chromium launch, but the browser executable was absent. Static structure/link checks passed; no browser-rendering test is claimed.

## Interpret the evidence correctly

The 143 Python cases and 200 C++ assertions are regression evidence for the included contracts, not a proof of all possible inputs. CTest reports one executable, not 200 independent test executables. Included CPU timings are local single-run diagnostics and do not establish future engine performance. All learner completion statuses remain learner work. See raw logs for exact commands, measured environment and limitations.
