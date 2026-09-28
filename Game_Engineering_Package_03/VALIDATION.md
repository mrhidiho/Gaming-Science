# Package 03 validation record

Edition: September 28, 2026. This record describes tests of the supplied reference material, not completed student work.

## Code executed
The full reference suite passed **230 test methods** using **Python 3.13.5 on Linux x86_64**: 169 designated lab-contract cases, 33 further property/integration checks, eight deliberate-mutant detection checks, and 20 executed demonstration/output checks. All 20 example programs also passed the standalone expected-output runner. Core scripts use the standard library. The optional illustration renderer was run with Matplotlib 3.10.8.

The mutant checks verify that selected intentionally wrong implementations are caught. They do not establish complete mutation coverage or prove a theorem. The untouched student 06.1 file was checked and intentionally failed with NotImplementedError, as documented. Student implementations remain unfinished exercises.

## Source continuity and assessment counts
Compared programmatically against the supplied original curriculum: all 20 lesson identifiers, titles, outcomes, original labs, original reading strings and first three quiz questions/answers are preserved. Original module prerequisites and project briefs are retained. The source excerpt identifies that its retained global 200/600 counts refer to the original complete program, not the math subset.

This bundle contains 100 lesson questions (60 retained, 40 added), 25 module-review questions, 75 written problems, ten algebra-bridge items and 20 independent-transfer tasks. The PDF answer labels and problem/review IDs were checked against the structured data. Every student/reference lab pair and every example file was found.

## Numerical and measured evidence
The model-evidence generator ran successfully. Ten deterministic data files, excluding variable metadata, reproduced byte-for-byte in a fresh extraction on the same interpreter/environment. This is not a promise of cross-version random streams or arbitrary-platform floating-point identity.

The included benchmark contains **360 real timing observations**: six workloads, 30 paired trials and two methods. Correct results were checked independently. A fresh-extraction run with ten pairs produced 120 new observations, with all output checks passing. Reusing its existing destination directory was correctly rejected. The measured times are local Python microbenchmark data, not hardware ratings or native-engine/GPU measurements. Its Student-t intervals are conditional on sampling assumptions, which the runner does not automatically establish.

Synthetic frame-time/regression examples and model/sampling outputs are labeled separately from actual measured timings. Their labels are part of the evidence contract; no real-player telemetry was collected.

## PDF review
All 12 PDFs were rasterized with PyMuPDF, covering **235 pages including repeated material in the individual module PDFs**. Automated text and image bounding-box checks reported no elements outside the checked page/content margins and no replacement-character findings. Contact sheets and representative full-size pages were reviewed, including formulas, code, tables and illustrations. A PDF image-sizing issue was caught and corrected before the final render. PDF bookmarks and table-of-contents links were generated; the PDFs are not claimed as a fully tagged accessibility-compliance artifact.

Final main-document lengths: Student Handbook 77 pages; Lab Workbook 30; Answer Key 35; Start Next 4; Gate B Specification 7; Mathematical Reference 4. The five separate module PDFs are 14, 15, 15, 14 and 16 pages. The supplied Reference Notebook is four pages. Repeated content should not be counted as extra lessons.

## Browser review
Tested with Chromium 144.0.7559.96 through Playwright on Linux. Managed Chromium blocked file:// navigation with ERR_BLOCKED_BY_ADMINISTRATOR, so the actual HTML was tested using an in-memory document. Tests covered 20 rendered lessons; five embedded figures; successful and empty-result searches; clearing search; collapsed/expanded answers; quiz/evidence progress conditions; JSON download/export and import; invalid-package and out-of-range-score rejection without loss of existing in-page progress; and desktop plus 390-pixel mobile layouts. No page-level horizontal overflow or browser page errors were observed in those tests.

**Direct opening as a local file and persistence through local-file reload were not verified.** Storage behavior can differ across browsers and contexts. The page handles unavailable storage and supports progress export/import. No claim of a cross-browser, screen-reader or long-term storage audit is made.

## Fresh archive and reproduction
A candidate ZIP passed CRC integrity checking, was extracted into a new directory, and passed the 230-reference-test suite again, all 20 examples, the environment check, numerical regeneration and a new measured benchmark run. The final archive is also checked after the validation/manifest files are added. It excludes caches, temporary renders, private work scripts and standalone font files.

Use `python tools/verify_manifest.py` to compare an unmodified extraction against the supplied SHA-256 inventory. The manifest excludes itself. A checksum is not a cryptographic signature or an authenticity guarantee; intentional learner edits should change the corresponding hashes. Unlisted generated outputs are not hashed.

## Scope not established by these checks
No independent student proof review, project defense or external expert review has already happened. Testing does not prove every input, sampling assumption or algorithmic property. Windows, macOS, alternate interpreters, native engine integration, actual GPU execution and physical hardware were not tested. Workload durations on another system may differ substantially. The learner must complete the assignments and obtain the required review.
