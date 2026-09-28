# Package validation report

Edition: September 28, 2026. These are tests of the distributed teaching package, not independent validation of a learner thesis or a real hardware product.

## Executed and passed

| Check | Actual result | Evidence |
|---|---|---|
| Python reference suite | 83 test methods passed; zero failures/errors/skips | `python_tests.json`, `python_tests.log` |
| C++17 build and CTest | GCC build succeeded; 3 of 3 checks passed | `cpp_build.log`, `cpp_tests.log` |
| Deterministic demonstration outputs | All 13 regenerated files matched byte-for-byte in a new directory | `demo_reproduction.json` |
| Curriculum continuity | 20 IDs, titles, outcomes, assignments and readings match the original volume; 60 question/answer pairs | `metadata/CONTINUITY.md`, original volume metadata |
| Python source syntax | All 20 distributed Python sources parsed | `browser_checks.json` records this source check |
| Browser static checks | Seven HTML entry/content pages have valid local paths/anchors; JavaScript parses | `browser_checks.json` |
| Browser UI exercise | 20 lessons, search/reset, read count, storage fallback, answer content and responsive layout checked in Chromium | `browser_checks.json` |
| PDF checks | Six PDFs, 122 pages; all pages rasterized; text bounds and quiz grouping checked | `pdf_checks.json` |

The Python suite includes finite exhaustive subcases: 46,656 length-six atomic MSI request traces and the ECC exercise’s 16 clean, 128 single-bit and 448 double-bit cases. These are subcases, not separately named test methods. The abstract queue exploration reaches seven states under its stated capacity and alphabet. None of those finite results is an unrestricted claim about an industrial protocol.

## Actual environment

Python: 3.13.5 (main, Jul 15 2026, 20:25:40) [GCC 14.2.0]. Platform: Linux-6.18.44-x86_64-with-glibc2.41; architecture: x86_64. C++ compiler: GCC 14.2.0. CMake: 3.31.6. The C++ project requests C++17 and builds with warnings treated as errors. The browser UI was exercised in Chromium 144.0.7559.96. Exact tool-availability details are in `environment.json`.

The core Python code’s declared language baseline is 3.10+, but only the recorded interpreter and operating system were executed. No Windows, macOS, alternate Python-version or alternate C++-compiler pass is claimed. No executable binaries or external toolchains are shipped.

## Browser test boundary

The browser environment blocked both local-file and localhost navigation by policy. UI testing therefore injected the actual page markup, local CSS and JavaScript through Playwright’s page-content interface. Search, display, read-count updates and the graceful local-storage-unavailable fallback passed. Native persistent storage across reload and file/HTTP navigation were not exercised. Static file and anchor checks were performed separately. The reader remains usable without progress storage; `templates/PROGRESS.md` is the evidence-based alternative.

## Not executed here

Icarus Verilog simulation, Yosys/SBY/SMT proof and cover tasks, OpenSTA timing and the OpenROAD physical flow were not run because their required tools were unavailable. The associated source, testbench, properties and configurations are supplied as learner-run teaching inputs. No HDL simulation pass, completed formal proof, routed PPA result, DRC/LVS signoff or silicon validation is represented by the Python tests.

The student function route is intentionally unfinished and expected to fail until implemented. That is a teaching condition, not a reference regression. Real game-engine benchmarks, analog CDC reliability, power measurements and a thesis experiment were not performed. Every distributed demonstration dataset is marked synthetic.

## PDF and integrity interpretation

All PDF pages were rasterized with `pdftoppm`; overview sheets and selected high-resolution pages were visually inspected. Automated checks found no text outside the declared page bounds, missing-character placeholders or split three-question quiz groups. Page counts include covers and contents. These layout checks do not independently certify every pedagogical or technical claim.

`FILE_MANIFEST.json` inventories relative paths, lengths and SHA-256 hashes. `VALIDATE_PACKAGE.py` checks them and the lesson/quiz counts without network access or writes. The manifest cannot hash itself and is not proof of authenticity, truth or academic achievement. After editing an inventoried file, a mismatch is expected; use a clean release to compare and keep your work separately.

## Reproduction commands

From the extracted root:

```sh
python code/run_tests.py
python code/demo.py --out my_evidence/reference_outputs
cmake -S code/cpp -B my_evidence/cpp-build -DCMAKE_BUILD_TYPE=Release
cmake --build my_evidence/cpp-build
ctest --test-dir my_evidence/cpp-build --output-on-failure
python VALIDATE_PACKAGE.py
```

The C++ route requires its toolchain; the Python routes require no third-party packages. The separate `code/rtl/README.md` describes optional hardware-tool routes and their additional review obligations.
