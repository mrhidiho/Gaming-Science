# Game Engineering - Package 02

## Expanded Volume 1: Foundations and Your First Game

Start with START_NEXT.pdf. Open COURSE.html for the searchable learner edition.

This expands the first volume of the original all-program starter; it is not a second mathematics volume. It preserves Modules 01-05 and lessons 01.1-05.4. First-day lessons already completed can be reviewed through the new application questions before continuing at 01.3.

## Main files

- STUDENT_HANDBOOK.pdf: full explanations, 20 worked examples, practical briefs and 100 lesson quiz questions.
- LAB_WORKBOOK.pdf: 20 practical worksheets, 50 additional exercises, five integration projects and 25 module-review questions.
- ANSWER_KEY.pdf: explanatory quiz/review answers, exercise solutions/guidance and practical review notes.
- CAPSTONE_SPEC.pdf / .md: exact Gate A rules, milestones, schemas, tests and rubric.
- modules/: five smaller printable teaching PDFs.
- examples/: 20 executable demonstrations, including deliberately labeled bug/review cases.
- labs/student/: 16 intentionally unfinished function exercises.
- labs/reference/: 16 completed reference solutions.
- capstone/student/: intentionally unfinished project and test scaffolds.
- capstone/reference/: completed comparison game, not a student submission.
- tools/: environment report, contract checker, game tests, Git sandbox, mutation example and benchmark.
- templates/: seven Markdown worksheets plus a JSON progress template.
- source/ and lessons/: editable material and machine-readable package content.
- validation/: actual test/example logs and a sample benchmark report.
- PACKAGE_MANIFEST.json: inventory, counts, original-curriculum identity and file checksums.

## Run locally

From this extracted folder, use a verified Python 3 launcher (python3 on many macOS/Linux systems; py -3 or python on Windows):

```sh
python3 tools/environment_check.py
python3 examples/example_01_3.py
python3 tools/check_labs.py --lesson 02.4
python3 tools/check_labs.py --reference
python3 capstone/reference/play.py --demo
python3 tools/check_game.py
```

The student check is expected to fail until that starter is implemented. Reference-mode success does not test your changes. Four labs require manual evidence rather than a function checker. The student capstone test deliberately fails until replaced with real tests.

No runtime third-party Python packages are required. Git is needed at 04.3. The executed environment and limits are in VALIDATION.md. External readings retain their authors' rights and are linked rather than copied. No font files, proprietary SDKs or external textbooks are distributed.

## Progress and completion

COURSE.html stores self-recorded progress locally when browser storage is available. Export regularly; moving the file or changing browsers can change the storage context. Import validates the schema and asks before replacement. Progress is not sent to a server and does not automatically inspect code.

Attempt answers before opening ANSWER_KEY.pdf. Complete the original core quiz threshold, the new application questions, labs, changed cases, module exercises and projects. The package is a self-study educational resource, not an accredited degree or a guarantee of professional competence.
