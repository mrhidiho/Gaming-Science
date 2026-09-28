# Game Engineering — Package 04

## Expanded Volume 03: C++, Algorithms and Language Implementation

Start with **START_NEXT.pdf** or open **COURSE.html** in a browser. Extract the whole ZIP before running code. This package expands Modules11–15 and GateC; it does not replace Package03 (mathematics).

Included:20 expanded lessons;100 lesson questions (60 original +40 new);20 reference lesson programs;20 unfinished student contracts;40 extra exercises with solutions;25 module reviews;five module projects feeding GateC;four C17/C++ bridge exercises and12 bridge questions;seven main PDFs, five module PDFs, offline reader, editable source and eight templates.

Use a C++20/C17 compiler and CMake3.20+. No GPU or external code library is required. Python helpers are optional. From this folder:

```sh
cmake -S code -B build/debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build/debug --config Debug --parallel 2
ctest --test-dir build/debug -C Debug -L reference --output-on-failure
```

The default24 reference programs should pass. Student starters intentionally compile but fail until implemented; follow the full workbook contract, not just starter checks. See START_NEXT.pdf for the separate student workflow, Release and sanitizers.

Read VALIDATION.md for actual tested configurations and limitations. MANIFEST.json inventories files and hashes; code/tools/verify_manifest.py checks them before local edits. External references are linked, not copied. Reference code is educational, not a production engine, secure scripting sandbox or completed student capstone.
