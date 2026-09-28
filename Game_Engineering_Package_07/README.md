# Package 07 — Volume 06
## Game Systems and Production

Modules 26–30 · Lessons 26.1–30.4 · Gate F

Extract the complete archive and keep its folders together. Begin with START_NEXT.pdf, then STUDENT_HANDBOOK.pdf or COURSE.html. Answers are separate in ANSWER_KEY.pdf and closed by default in the browser course.

## Main documents

| File | Pages | Purpose |
|---|---:|---|
| START_NEXT.pdf | 6 | Sequence, setup, first session and assessment |
| STUDENT_HANDBOOK.pdf | 79 | 20 expanded lessons, worked examples, quizzes, projects and reading |
| LAB_WORKBOOK.pdf | 50 | 20 complete lab cards, kernel contracts, adversarial tests and evidence |
| ANSWER_KEY.pdf | 30 | 100 lesson answers and 25 module-review answers |
| CAPSTONE_SPEC.pdf | 9 | Gate F game scope, milestones, acceptance matrix and review |
| SYSTEMS_REFERENCE.pdf | 12 | Formulas, units, conventions and subsystem boundaries |
| NATIVE_INTEGRATION_GUIDE.pdf | 11 | C++/platform transfer, build commands and evidence limits |

The five module PDFs under modules/ repeat the relevant handbook material with a reference directory for independent use. Their page counts are not additional unique curriculum content.

## Scope

26: collision, rigid-body/rotational impulses, constraints, continuous detection and deterministic testing.

27: hierarchies/skinning, blending/IK, real-time audio discipline, spatial cues and multimodal feedback.

28: navigation/steering, inspectable decisions, bounded adversarial search and responsibly evaluated learning.

29: authority/prediction, interpolation/relevance, rollback/lockstep and recoverable services.

30: profiling, compatibility/accessibility/localization, packaging/mod boundaries and the undergraduate game capstone.

## Included teaching assets

20 expanded lessons; 20 full lab cards; 100 lesson questions (60 original plus 40 application); 25 module-review questions; five integrating module projects; 20 runnable Python demos; 20 deliberately unimplemented exercises with 20 reference solutions; 98 contract cases; 17 invariant/oracle test methods; five runnable integration companions; one native C++17 offline audio harness; fourteen blank Markdown evidence templates and a JSON progress template; editable Markdown/JSON; and a self-contained browser course.

The five projects culminate in Gate F. Do not count Gate F as an unrelated sixth large project. The original 420–650 planning-hour estimate includes study, implementation, integration and review, not reading time or academic credit.

## Run the supplied checks

```text
python starter/run_all.py
python starter/run_all.py --native
python verify_manifest.py
```

The native option additionally requires CMake/CTest and a C++17 compiler. Python uses standard-library-only examples with a 3.11+ syntax baseline; actual tested versions/platform are recorded in evidence/TESTED_ENVIRONMENT.md.

To work on one exercise:

```text
python starter/python/demos/lesson_26_1.py
python starter/python/run_tests.py --target exercises --lesson 26.1
```

The exercise fails until implemented. Read the full workbook lab; a passing kernel is only one part of it. Do not import the reference into your solution.

## Browser course and progress

Open COURSE.html in a browser after extraction. All lesson/lab/answer content and interface code are embedded; the PDF shortcut links assume the surrounding package files are present. Search, expand answers after attempting questions and export progress JSON regularly. Browser file-storage behavior varies; when persistent storage is unavailable the UI retains the current session in memory and supports export/import.

The automatic UI checks in this environment used direct document-content rendering because administrative browser policy blocked file and loopback HTTP navigation. Search, reveal, progress export/import, invalid-import rejection, reset, storage-failure handling and narrow-screen layout were tested. Native local-storage persistence, file-link navigation and all-browser compatibility were not verified here.

## Evidence boundaries

All 98 reference cases, 17 property methods, 20 demos, five companions and native offline checks passed in the documented environment. The property suite includes 700 seeded randomized scenarios across six methods. These are not completed student labs or a finished game.

Actual platform audio/device stress, maintained physics-library comparison, the learner’s native engine implementation, local process/socket multiplayer, registry integration, target-device frame/inference measurements and independent human review remain learner requirements. Offline audio is not an underrun proof; in-process transport is not a socket test; exception-injected replacement is not power-loss certification. See the workbook and capstone specification.

## File integrity

MANIFEST.json records package counts, page counts and SHA-256 for packaged files. The manifest excludes itself from its checksum list. verify_manifest.py checks file contents against that list; it does not establish publisher authenticity. Editing an exercise or source document legitimately changes its hash.

This is an expanded self-study curriculum, not an accredited degree. No finished student capstone, fabricated human review, public server or paid account is supplied or required by the core demonstrations.
