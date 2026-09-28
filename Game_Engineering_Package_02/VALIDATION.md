# Package 02 validation record

Edition: September 28, 2026. This record describes checks of the supplied artifacts, not assessment of a student or an accredited course.

## Executed environment

Python 3.13.5 on Linux in the preparation container. The code targets Python 3.11 or later using the standard library; only Python 3.13.5 was executed here. Windows and macOS command forms are provided, but were not executed on those operating systems. The environment report records the exact interpreter and Git availability. Git is needed only for the Git exercise.

## Code checks

| Check | Observed result |
|---|---|
| Reference function contract suite | 123 unittest test methods passed |
| Reference Training Yard game suite | 59 unittest test methods passed |
| Total reference test methods | 182 passed; loops inside some tests add cases, not separately counted methods |
| Worked demonstration files | All 20 executed with exit code 0 |
| Python source compilation | All packaged Python files compiled successfully; intentional TODOs are syntactically valid |
| Deliberate double-damage mutation | Rejected by the demonstration test; this does not establish mutation coverage |
| Git sandbox | Completed branch, merge and revert exercise in an isolated temporary repository |
| Benchmark | Completed warm-up and seven timed trials; raw sample retained, not a performance guarantee |
| Fresh-copy reference runs | Lab suite, game suite and demonstration passed from a new temporary root |
| Student 02.4 starter | Expected nonzero result with NotImplementedError, both before and after copying |

See `validation/lab_tests.txt`, `game_tests.txt`, `example_runs.json`, `mutation_demo.txt`, `git_sandbox.txt`, `benchmark_example.json` and `clean_copy_checks.json`. Counts describe methods, not proof of complete correctness. A reference check does not execute the student's independent capstone. Four evidence-oriented labs require manual work and review. The student capstone's placeholder test deliberately fails until replaced with meaningful tests.

## Document and curriculum checks

All 20 lesson IDs, titles and learning outcomes match the original Volume 1 source. The original three quiz questions per lesson are retained; two application questions per lesson are added. Counts: 100 lesson questions, 25 module reviews and 50 additional exercises. There are 20 lab briefs, 16 automated exercise pairs, four evidence-based labs, five integration projects and 18 companion-source entries. The original curriculum SHA-256 is recorded in the manifest.

The PDFs were rendered with PDFium and reviewed through contact sheets and selected larger page views. Text-bound checks found no blocks outside the page-margin threshold. Covers, contents, lesson pages, code blocks, quizzes, tables and answer layouts were inspected. This is a layout and content-consistency review, not independent academic peer review.

| PDF | Pages |
|---|---:|
| `ANSWER_KEY.pdf` | 43 |
| `CAPSTONE_SPEC.pdf` | 8 |
| `LAB_WORKBOOK.pdf` | 28 |
| `START_NEXT.pdf` | 4 |
| `STUDENT_HANDBOOK.pdf` | 66 |
| `modules/MODULE_01.pdf` | 14 |
| `modules/MODULE_02.pdf` | 14 |
| `modules/MODULE_03.pdf` | 14 |
| `modules/MODULE_04.pdf` | 14 |
| `modules/MODULE_05.pdf` | 14 |

The five module PDFs duplicate their sections of the student handbook; do not count them as additional lessons or unique teaching pages. The answers remain outside the student handbook and reader.

## Browser checks and limits

The supplied self-contained HTML was exercised in Chromium 144.0.7559.96 with Playwright. Checks covered 20 lesson articles, search/clear, score thresholds, study/lab flags, JSON export, rejection of invalid imports, confirmed valid imports and desktop/mobile overflow. No JavaScript errors occurred in that test.

The managed browser blocked both direct `file://` and loopback HTTP navigation. Testing therefore injected the supplied HTML into an in-memory page. Direct file navigation, reload persistence and browser-specific local-file storage were **not verified** here. The reader handles unavailable storage by asking the learner to export progress. Keep regular exports; do not assume moving the HTML preserves its browser storage. Detailed results are in `validation/reader_checks.json`.

## Intentional limitations

The reference game is an educational terminal program, not a game engine. Save validation checks schema and stated invariants, not that every state has a legitimate gameplay history. File replacement tests do not establish universal power-loss durability. Benchmark results measure the stated Python update workload, not graphics frame rate or another computer's performance. The supplied tests and examples are not substitutes for the learner's own tests, explanation, changed-case work and independent review.

External readings are linked, not bundled. No font files, proprietary SDKs, virtual environments or private credentials are distributed. `data/truncated_save.json` is intentionally malformed test input. Student TODOs and the deliberately failing starter test are intentional, clearly separated from passing reference implementations.
