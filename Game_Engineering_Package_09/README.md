# Game Engineering — Package 09 / Expanded Volume 08

**Gaming Platforms and Hardware/Software Co-design.** Modules 36–40, lessons 36.1–40.4, Gate H. Start with START_NEXT.pdf, then STUDENT_HANDBOOK.pdf and LAB_WORKBOOK.pdf. Open COURSE.html for the offline edition; reveal answers only after attempting them.

## Files
- STUDENT_HANDBOOK.pdf: all 20 expanded lessons and 100 lesson questions.
- LAB_WORKBOOK.pdf: original practical requirements, computational contracts, full lab steps, 40 written problems, 25 module reviews and five projects.
- ANSWER_KEY.pdf: explained answers, written solutions and diagnostic/review guidance.
- CAPSTONE_SPEC.pdf: requirements, milestones, test matrix and Gate H rubric.
- PLATFORM_REFERENCE.pdf: units, formulas, contracts and glossary.
- REFERENCE_CASE_STUDY.pdf: the runnable teaching example, explicitly not a completed learner Gate H.
- source/: editable Markdown and machine-readable JSON, including original volume/quiz metadata.
- labs/: demos, student starters, reference implementations and tests.
- capstone/: functional pipeline, optional native C++ baseline, runner, auditor and edition results.
- data/: contract cases and explicitly synthetic power/latency traces with generator and provenance.
- templates/: portfolio, experiment, interface and review templates.
- validation/: actual test logs and package validation results.

## Run from this folder
```text
python -m labs.run demo 36.1
python -m labs.run check 36.1 --student
python -m labs.run all
python -m unittest discover -s labs/tests -v
python -m capstone.run_capstone --output my_results/model_only
python -m capstone.audit my_results/model_only/evidence_ledger.json
python -m capstone.sensitivity --input my_results/model_only/model_results.json --output my_results/model_only
```
Use python3 or py instead of python where appropriate. The core code uses only the Python standard library. Python 3.11+ is the selected syntax baseline; execution was tested on Python 3.13.5/Linux. Untouched student starters intentionally fail. Add --native to the capstone command only with an existing C++17 compiler. Use a new output folder to preserve supplied measurements.

## Scope
The original 350–560-hour planning range includes assigned study, full practical work, projects and revision. Model checkers do not replace the original KiCad, engine-investigation or capstone requirements. No new physical hardware is required. Physical work is optional and reviewed; no board, GPU accelerator or XR device was tested here. Model clock/bandwidth/resource values are not physical measurements. This is self-study, not an accredited degree or production signoff.

Read SOURCES.md and the validation report before interpreting results. The source directory identifies preserved original curriculum metadata and added teaching material. No external manuals, proprietary SDKs, credentials or font files are bundled.
