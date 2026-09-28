# Package validation report

Package 09 / Volume 08 — edition September 28, 2026.

## Results

**PASS — Original manifest and quiz continuity.** All 20 IDs, titles, outcomes, practical briefs, assigned readings and first three quiz questions match the original source.

**PASS — Assessment counts.** {"modules": 5, "lessons": 20, "lesson_questions": 100, "original_lesson_questions": 60, "added_lesson_questions": 40, "module_review_questions": 25, "written_problems": 40, "diagnostic_questions": 10, "module_projects": 5}

**PASS — Python syntax.** 75 Python files parsed with 3.13.5.

**PASS — Runnable demonstrations.** All 20 demo files executed successfully from an unrelated temporary working directory.

**PASS — Unimplemented student starter.** Expected failure confirms the CLI tests the student route; untouched starters are intentionally incomplete learning exercises.

**PASS — Automated unit suite.** 148 tests pass, including 128 declared contract cases and additional arithmetic, flow-control, ownership-audit and sensitivity checks.

**PASS — Retained native baseline evidence.** {"raw_rows": 420, "retained_samples": 360, "warmup_rows": 60, "compiler": "g++ (Debian 14.2.0-19) 14.2.0", "boundary": "C++ host function only; allocation, validation and checksum outside timing"}

**PASS — Pipeline reference cases.** 36 cases rerun after independent packet-arithmetic implementation; retained modeled values and trace reproduced exactly.

**PASS — Sensitivity grid.** 36 functional trace configurations × 27 analytical parameter combinations; no new hardware measurements.

**PASS — Synthetic trace consistency.** {"power": {"joules": 6600.0, "duration_s": 120, "average_w": 55.0, "frames_per_joule": 0.9545454545454546}, "latency": {"mean_latency_ms": 50.0, "p95_latency_ms": 66.6666666670003, "min_interval_ms": 16.666666665999855, "max_interval_ms": 33.33333333400003, "mean_rate_fps": 59.337016574579074, "boundary": "synthetic_present"}, "scope": "Explicitly synthetic; interval-average watts and software markers."}

**PASS — HTML unique anchors.** 82 distinct IDs.

**PASS — HTML links and answer reveal structure.** 175 answer panels are initially closed; local links and internal anchors resolve.

**PASS — Chromium behavior.** {"browser": "Playwright with system Chromium; supplied HTML set_content (container policy blocks file:// navigation)", "executed": true, "sections": 36, "answer_details": 175, "all_answers_initially_closed": true, "search_no_match_clear_navigation": true, "matching_sections_for_quiescence": 7, "answer_reveal_close": true, "javascript_errors": [], "viewports_tested": [[1440, 1000], [390, 844]], "limits": "HTML content, search, anchors and reveal behavior checked via set_content; direct file:// opening was blocked by container browser policy. External reading sites and other browser engines not tested."}

**PASS — PDF structural checks.** {"pdf_files": 7, "total_pages": 163, "outside_page_spans": [], "replacement_or_nul_glyphs": []}

## PDF inventory

| File | Pages |
|---|---|
| ANSWER_KEY.pdf | 30 |
| CAPSTONE_SPEC.pdf | 9 |
| LAB_WORKBOOK.pdf | 53 |
| PLATFORM_REFERENCE.pdf | 7 |
| REFERENCE_CASE_STUDY.pdf | 6 |
| START_NEXT.pdf | 6 |
| STUDENT_HANDBOOK.pdf | 52 |

## Visual review

PDF contact sheets and representative full-size pages inspected in PyMuPDF raster output; browser content inspected at desktop/mobile widths. No overlap, clipping or missing-glyph issue found in reviewed pages. Workbook continuation whitespace remains available for learner notes.

## Important limits

- Core Python execution tested on Python 3.13.5/Linux, not every supported syntax-baseline version or operating system.
- Native C++ data are actual build-host function measurements; not physical accelerator, whole-game, optical latency or another machine’s measurements.
- Model clocks, bandwidths, resource counts and sensitivity are explicit assumptions/estimates; no synthesis, FPGA/GPU execution, board bring-up, KiCad GUI or XR runtime was tested.
- Browser interactions tested through supplied HTML content in system Chromium; direct file:// navigation was blocked by container administrator policy. External links and other browsers were not exercised.
- Published tests and hash checks do not constitute formal verification or scientific peer review. Full original practical work and the learner Gate H remain learner assignments.
