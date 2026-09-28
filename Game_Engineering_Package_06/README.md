# Package 06 - Volume 05: Graphics and Game-Engine Construction

This is the expanded teaching bundle for Modules 21-25 and Gate E. It preserves the roadmap's lesson IDs, titles, outcomes, original lab assignments, original reading assignments and first three quiz questions. It adds original teaching, worked examples, two application questions per lesson, module reviews and implementation exercises.

## Open first

Read START_NEXT.pdf, then STUDENT_HANDBOOK.pdf. COURSE.html is the offline searchable edition. LAB_WORKBOOK.pdf contains procedures and pass criteria; ANSWER_KEY.pdf is separate. CAPSTONE_SPEC.pdf defines the learner's integrated engine and independent review. ENGINE_REFERENCE.pdf records technical contracts, backend mapping, file formats and code scope. The source/ folder contains editable Markdown and JSON; modules/ contains five smaller teaching PDFs.

## Begin without a GPU

From this extracted folder, use a Python 3.11+ interpreter (on Windows, `py -3` may replace `python`):

```sh
python tests/test_exercises.py --track reference
python code/python/run_examples.py
python tests/test_exercises.py --track starter --lesson 21.1
```

The last command deliberately fails until you implement the starter. Edit exercises/starter/lesson_21_1.py, not the reference implementation. The tests must be pointed at --track starter to grade your work. Passing the supplied reference tests does not complete a lesson.

## Build the C++ reference

C++20 and CMake 3.20+ are the selected language/build baselines, not claims of separately tested compatibility on all versions or operating systems.

```sh
cmake -S code/cpp -B work/cpp -DCMAKE_BUILD_TYPE=Release
cmake --build work/cpp --config Release
ctest --test-dir work/cpp -C Release --output-on-failure
./work/cpp/cpu_renderer --output work/reference.ppm
./work/cpp/cpu_renderer --affine --output work/affine.ppm
```

With a multi-configuration Windows generator, the executable is typically work/cpp/Release/cpu_renderer.exe. Use the actual generated path. CPU outputs are an explicitly documented sRGB-coded PPM variant. Included PNG previews in evidence/ can be viewed without a PPM-capable viewer. No GPU or downloaded dependency is needed for these reference checks.

## Reproduce the CPU validation

```sh
python validate_all.py
```

This writes fresh results to work/validation, builds C++, cooks original assets, runs the sphere BVH comparison, renders images and checks JavaScript syntax when Node is installed. `--skip-cpp` permits Python-only work and marks C++ skipped. It never executes WebGPU. See validation/ for the actual package-authoring run and TESTED_ENVIRONMENT.json for versions and exclusions.

## Cook assets and use the native mesh

```sh
python code/python/cook_assets.py --source assets/source --out work/cooked
```

The command prints the exact content-addressed `.gem` path. Pass that path to `cpu_renderer --mesh PATH --output work/cooked.ppm`. The `.get` mip payload is built and tested but is NOT sampled by the current C++ renderer; implementing that sampler is learner integration work. The renderer uses a procedural point-sampled checker and unlit vertex colors. It is not a completed PBR renderer.

## Optional WebGPU bridge

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory code/webgpu
```

Open http://localhost:8000 in a compatible browser. Do not open the demo with a file:// URL. The page reports actual limits, compilation/validation messages and bounded compute readback, then transforms and draws a cube. It exercises two reusable contexts, depth, resize and explicit stop. Native barriers, a complete renderer backend, device-loss recovery and full engine integration remain learner work. Only JavaScript syntax was checked during packaging; no hardware run is claimed.

## Completion policy

There are 20 lesson labs, 100 lesson questions (60 preserved + 40 new), 25 module-review questions, 20 starter/reference exercise pairs and five integrating module projects. Gate E integrates those projects; do not count it as a sixth independent project. Planning allowance remains 420-650 hours including practice, projects and review; this is not reading time or a degree/credit claim.

Run every lesson's lab, explain the result, solve a new transfer problem and complete the applicable project. The supplied examples cover only selected contracts. PBR, temporal reconstruction, an interactive editor, a full asynchronous residency manager, a native GPU backend and the complete small engine are not supplied as finished products. Independent Gate E review has NOT been performed.

## Integrity and use

PACKAGE_MANIFEST.json and SHA256SUMS.txt enumerate payload files and their digests. The checksum file cannot hash itself. Use source/REFERENCES.md for original and supplemental reading provenance. No external fonts, textbooks, third-party art or proprietary SDK binaries are redistributed. Code and procedural assets are original educational examples provided for use and adaptation in your learning projects; no fitness or production-safety guarantee is made.
