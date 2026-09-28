# Game Engineering — Package 03
## Expanded Volume 02: Mathematics for Games and Computing
Start with START_NEXT.pdf or source/START_NEXT.md. This bundle follows Package 02 (expanded Volume 1), preserving Modules 06-10 and lessons 06.1-10.4. It does not renumber the original curriculum.

## Main documents
- STUDENT_HANDBOOK.pdf: 20 lessons, original outcomes, derivations, runnable demonstrations and five-question quizzes.
- LAB_WORKBOOK.pdf: 20 full practical briefs/coding contracts, 75 written problems, 25 module-review questions, ten algebra-bridge items and five integration projects.
- ANSWER_KEY.pdf: answers to 100 lesson questions, 25 review questions, 75 problems, ten bridge items and 20 independent-transfer tasks.
- CAPSTONE_SPEC.pdf: the original Gate B requirement and the expanded submission/review contract.
- MATH_REFERENCE.pdf: formulas with their domains and conventions.
- COURSE.html: standalone searchable lesson edition with local, self-recorded progress and export/import.
- modules/: five separate teaching PDFs.

There are 60 retained core lesson questions and 40 new application questions, not 100 wholly new questions. The 25 module-review questions are additional. The five module projects feed one Gate B notebook. Original external study remains required; these are self-study materials, not academic credits or an accredited degree.

## Required software and commands
Use a verified Python 3.11+ interpreter command. Tests were actually run with Python 3.13.5 on Linux. Substitute python3 or py -3 for python when that is the installed launcher. The core uses only the standard library.

```sh
python environment_check.py
python run_example.py 06.1
python run_example.py --all --verify
python check_lab.py 06.1
python check_lab.py --all --reference
python validate_reference.py
```

Student functions deliberately raise NotImplementedError until implemented. The first student-check failure is expected. Reference entry files import mathkit.py; demonstrations also use that supplied implementation. Do not import the reference to present it as completed student work.

```sh
python capstone/reference/build_evidence.py --out outputs/new_reference
python run_benchmark.py --out outputs/my_benchmark --pairs 30
```

Both generators require a new output directory and refuse to overwrite one. The numerical generator produces model/synthetic evidence. The benchmark measures the current machine and saves metadata, raw trials and a summary. Timings vary; they are not expected-output constants. Existing reference files are labeled by category, including synthetic teaching data under data/.

## Optional illustration regeneration
Existing PNGs are included and core work does not require plotting. To regenerate them, use the optional Matplotlib environment described in requirements-optional.txt, then run tools/render_figures.py. Its tested version is recorded, not recommended as universally newest. Review script output paths before overwriting generated illustration files.

## Assessment and maintenance
Core quiz questions 1-3 need at least 5/6, and all five need at least 8/10, plus study, practical work and independent transfer. Review quizzes suggest 8/10. The project requires 80/100 plus all essential evidence. Written proofs, numerical assumptions and statistical interpretations need review beyond automated tests.

Save learner work separately. The standalone HTML has no server or analytics and does not upload data. Local browser storage is best-effort; export progress backups. source/ includes editable Markdown, the full expanded JSON and the unchanged original module definitions in a labeled excerpt. SOURCES.md records provenance; VALIDATION.md records precisely what was tested. PACKAGE_MANIFEST.json inventories final files and hashes, excluding itself.
