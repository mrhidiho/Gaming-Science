# Volume 9 code laboratory

## Run the supplied references

Use a Python 3.11-or-newer interpreter. The package was actually tested with Python 3.13.5 on Linux x86_64; other Python/OS combinations remain unverified. The Python references use only the standard library. No package installation, account, API key or network access is required to run them.

From the extracted package directory:

```sh
cd code
python3 -m unittest discover -s tests -v
python3 run_experiments.py all --out ../evidence/my_run
```

On Windows, replace `python3` with your installed `py -3` command where appropriate. Keep your new output separate from `evidence/reference_run`. Runtime varies; the supplied scenes are intentionally small diagnostic workloads.

## Work before reading solutions

```sh
python3 check_exercises.py --lesson 41.2
```

Edit `exercises/lesson_41_2.py`, implement `solve`, and add independent edge tests. The checker returns exit code 2 for a pending starter, 1 for a failure, and 0 only when all selected visible cases pass. A single visible test is not a graduate assessment. Complete the full workbook procedure, original lab, reading, two problems and quiz as well. All 20 starters intentionally ship unfinished.

## Individual experiments

```sh
python3 run_experiments.py numerical --out ../evidence/numerical_run
python3 run_experiments.py parallel --out ../evidence/parallel_model
python3 run_experiments.py bar --out ../evidence/bar_run
python3 run_experiments.py render --out ../evidence/render_run
python3 run_experiments.py systems --out ../evidence/system_model
python3 run_experiments.py compiler --out ../evidence/compiler_run
```

`numerical` compares PCG with and without Jacobi scaling on known-solution diagonal systems. Add non-diagonal systems and measured setup/solve timing for the full lab. `parallel` records semantic checks and analytical scheduling traces; it does not execute on a GPU. `bar` compares a one-dimensional linear XPBD chain with an independently assembled dense implicit-Euler solve. `render` generates a small grayscale diffuse path-tracing diagnostic and known-integral trials. `systems` explores resource and lifecycle models. `compiler` checks a restricted unsigned expression transformation and emits inspectable C++.

## Native C++20 semantic reference

A C++20 compiler and CMake 3.16 or newer are required by the supplied build. These are build requirements, not claims that every compiler version has been tested.

```sh
cmake -S native -B build-debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build-debug --config Debug
ctest --test-dir build-debug -C Debug --output-on-failure
cmake -S native -B build-release -DCMAKE_BUILD_TYPE=Release
cmake --build build-release --config Release
ctest --test-dir build-release -C Release --output-on-failure
```

For a supported GCC/Clang toolchain, build sanitizers separately:

```sh
cmake -S native -B build-sanitize -DCMAKE_BUILD_TYPE=Debug -DENABLE_SANITIZERS=ON
cmake --build build-sanitize
ctest --test-dir build-sanitize --output-on-failure
```

On a single-configuration Linux/macOS build, run `./build-release/v09_native --bench > ../evidence/my_native_pairs.csv`. A multi-configuration build may place the executable in `build-release/Release/`. The 12 randomized-order pairs are within one process, not 12 independent machines or scenes. Inspect the generated assembly and a competent library baseline before claiming a useful optimization. Do not time sanitizer builds as production performance.

## Optional CUDA route

Read `gpu/README.md`. The CUDA source was not compiled or run during package validation. It is a staged reduction only, not the required complete reduction-plus-scan/compaction GPU project. Device barriers, synchronization, capabilities, memory safety and performance all remain to be validated on actual supported hardware.

## Contracts and limitations

PCG's standard guarantees require an SPD problem and a valid preconditioner. The implementation checks dimensions and detects some breakdowns; it is not a proof that an arbitrary matrix is SPD. The renderer has a fixed maximum path depth, black environment and scene-scale epsilon, and its preview PPM is tone-mapped. Compare linear JSON radiance, not PPM values. The reservoir is weighted selection, not complete ReSTIR. The inverse-albedo routine is not a trained network. The stream/store/lifecycle programs are small single-process models, not a production engine or consensus system. The restricted expression interpreter is not an OS sandbox, and the package does not execute a native JIT.

Every extension should state its input domain, numerical/semantic contract, resource bound, oracle, adverse case and timing boundary. Reference tests are examples of this discipline, not substitutes for your own implementation and independent review.
