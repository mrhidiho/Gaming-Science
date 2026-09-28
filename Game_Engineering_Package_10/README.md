# Package 10 / Volume 9
## Graduate Game-Engine and Graphics Engineering

Computer Science and Computer Engineering for Games. Edition: September 28, 2026.

Open **START_NEXT.pdf** first. **COURSE.html** is a self-contained offline browser course with search, closed-by-default answers and progress export/import. Extract the ZIP before opening files. No web server is required.

## Contents

- `STUDENT_HANDBOOK.pdf`: 20 expanded lessons, Modules 41-45, original 60-question quiz sequence, worked examples, reading and practice.
- `LAB_WORKBOOK.pdf`: 20 full lab procedures, acceptance checks, 40 graduate problems and five module projects.
- `ANSWER_KEY.pdf`: original quiz answers, problem solutions, diagnostic guidance and review notes. Attempt the work before opening it.
- `CAPSTONE_SPEC.pdf`: Gate I reproduction-and-extension project, rubrics, evidence requirements and independent review.
- `REFERENCE_GUIDE.pdf`: inherited source directory plus focused primary readings, source status and terminology.
- `modules/`: five standalone teaching PDFs.
- `source/`: editable Markdown, original Volume 9 data, expanded curriculum JSON and browser source.
- `code/`: standard-library Python references and tests, 20 deliberately unfinished warm-ups, C++20 semantic reference and optional unvalidated CUDA source.
- `templates/`: research, lab, capability, failure, progress and review records.
- `evidence/`: recorded small diagnostic experiments, with explicit evidence boundaries.
- `validation/`: actual validation logs and a package status report.
- `FILE_MANIFEST.json` and `SHA256SUMS.txt`: file inventory and integrity checks.

## Begin

```sh
cd code
python3 -m unittest discover -s tests -v
python3 run_experiments.py all --out ../evidence/my_run
```

The Python references need no third-party modules. Tested environment and pending device validation are stated in `validation/VALIDATION_REPORT.md`. For learner work, edit `code/exercises/lesson_41_1.py` and run `python3 check_exercises.py --lesson 41.1`. A pending starter intentionally returns exit code 2.

## Scope

Planning estimate: 550-850 hours including reading, derivation, implementation, experiments, revision and overlapping Gate I work. Prerequisites are the original prior gates/modules; this is not a beginner entry point. These materials are a self-study curriculum, not an accredited degree.

The package contains educational references and assignments, not completed learner submissions. CPU models do not establish GPU performance, the small path tracer is not complete ReSTIR, the bar is not 3D cloth, and the restricted DSL is not an OS sandbox. Independent Gate I review remains learner work. External books, papers and documentation are linked and retain their own rights; no external full texts or font files are distributed.
