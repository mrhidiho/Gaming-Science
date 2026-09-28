# Package 8 / Volume 7 - validation report
## Release identity
Edition: September 28, 2026. This report describes the supplied release, not the learner's future implementation. The package expands lessons 31.1-35.4 and Gate G without changing the original core question or answer wording.

## Executed checks
The supplied Python reference suite completed **74 unittest tests with PASS**. Read `python_tests.txt` for every test name and `python_validation.json` for the exact command, Python version, platform, exit status and elapsed time. The suite includes 32 directed G16 cases, 100 seeded random arithmetic programs, 512 exhaustive four-bit adder cases, all signed-eight-bit saturating-add pairs, rational nearest-even rescaling checks, 15,000 queue-model cycles, circuit and sampled-input calculations, and peripheral/memory/raster model tests.

The processor vector generator produced **52 software-reference cases: 32 directed and 20 seeded random**. Their assembly, images, expected retirement CSV and terminal state are under `cpu_vectors/`. Generation is not RTL simulation. The software frame and input CSV are also model outputs, not captures from hardware or RTL.

All 23 Python source files compiled as Python syntax. All JSON files parsed, all 20 lesson IDs matched the intended range, all 60 original core questions and answers matched the source curriculum, all 100 question IDs were unique, and every referenced lab file/path existed. See `content_validation.json`.

The six PDFs contain **144 total pages**. Every page was rendered with pdftoppm at 80 dpi. PDF text-bound checks found no text outside page bounds and no replacement-character glyphs. Bookmarks and linked contents are present. Rendered contact sheets and selected full-size pages were reviewed for layout. Source Markdown remains editable. See `document_statistics.json` and `pdf_validation.json`.

Browser interaction checks passed in Chromium 144.0.7559.96 for lesson search, answer reveal, core/transfer score updates, storage-denied messaging, progress export/import, wrong-volume import rejection, document links and a 390-pixel responsive layout. No JavaScript page error occurred in those tests. The authoring browser policy blocked both file and loopback navigation, so the page was loaded into an in-memory document for testing. **Native local-file storage persistence was not verified.** The export/import round trip was tested. See `browser_validation.json`.

## Not executed or not claimed
Icarus/vvp, Verilator, Yosys, ngspice and the formal toolchain were not available on PATH in the authoring environment. The included HDL, SPICE and synthesis runners record **NOT_RUN** when their tools are missing. No RTL compilation or simulation pass, SPICE execution, synthesis success, formal proof, routed device timing, physical measurement or FPGA-board result is claimed by this release.

The RTL reference sources and testbenches are provided for review and execution in the learner's configured environment. Treat any simulator-specific adjustment as a versioned change and rerun the independent comparisons. The formal harness is intentionally an instructional starter, with occupancy/stability properties and covers; complete ordering evidence is learner work.

## Completion boundary
The course materials are supplied. Student circuit notebooks, independent implementations/modifications, pipeline and delayed-memory integration, full formal exercise, capstone adapter, actual RTL/synthesis evidence and oral reviews remain assignments. Supplied reference files are not pre-passed student submissions. Physical deployment is optional; simulator and synthesis evidence remain part of the required digital-design work.

## Reproduction commands
Run from the extracted package root:

```sh
python3 tools/verify_package.py
python3 tools/preflight.py
python3 tools/run_python_tests.py
python3 tools/generate_cpu_vectors.py
python3 tools/run_hdl.py
python3 tools/run_synthesis.py
python3 tools/run_spice.py
```

The last three commands require separately installed tools and return exit code 2 when unavailable. A failing executed check is not a skip. Preserve original release evidence before rerunning: commands intentionally replace their associated evidence outputs, after which the original release checksums will report those files as changed.
