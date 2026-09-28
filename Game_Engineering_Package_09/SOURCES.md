# Sources and provenance

## How references are used
The original curriculum's R-codes are retained for assigned study. S-codes identify selected official documentation and primary references checked while preparing this expansion on September 28, 2026. Moving documentation can change; use the version appropriate to the installed tool or target. A versioned KiCad 9.0 link is a deliberate teaching reference, not a claim about the latest release. No third-party manuals or proprietary SDKs are redistributed.

Original lesson IDs, titles, outcomes, practical briefs, assigned readings, module projects and first three quiz questions come from the supplied Game_Engineering_Program_Manifest.json and COMPLETE_CURRICULUM.pdf. The extracted Volume 08 manifest, original quiz text and complete original R-code directory are retained in source/ORIGINAL_VOLUME_08_MANIFEST.json. New explanations, worked examples, code, exercises, added questions and synthetic traces are original teaching material in this expansion. They do not imply accreditation or independent peer review.

Numerical examples labeled hypothetical or synthetic are not product specifications. The native reference measurements were actually executed on the build host; their method and limitations are in capstone/results/environment.json. No board, GPU accelerator, headset, KiCad GUI or proprietary console SDK was executed as part of this package's automated validation.

## Selected official and primary sources

**S01 — Zephyr Project: SPI peripheral API.** Role, mode and transaction vocabulary. Use the exact device datasheet for electrical limits.

<https://docs.zephyrproject.org/latest/hardware/peripherals/spi.html>

**S02 — Zephyr Project: Scheduling.** RTOS scheduling mechanisms; the supplied integer-tick scheduler is an original simplified model.

<https://docs.zephyrproject.org/latest/kernel/services/scheduling/index.html>

**S03 — KiCad Project: Schematic Editor, version 9.0.** Schematic editing and electrical-rule checking. Versioned documentation, not a claim that 9.0 is the latest release.

<https://docs.kicad.org/9.0/en/eeschema/eeschema.html>

**S04 — KiCad Project: PCB Editor, version 9.0.** Board layout and design-rule checks. Use documentation matching the installed version.

<https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html>

**S05 — Linux kernel contributors: Dynamic DMA mapping guide.** Mapping, access and ownership considerations. The educational Python code does not use DMA.

<https://docs.kernel.org/core-api/dma-api-howto.html>

**S06 — NVIDIA: CUDA Programming Guide: Writing SIMT Kernels.** GPU execution-group vocabulary; architecture parameters must be checked for the selected target.

<https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html>

**S07 — NVIDIA: CUDA C++ Best Practices Guide.** Performance, memory access and validation context. No CUDA runtime is required for the core labs.

<https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html>

**S08 — NVIDIA: CUDA Programming Guide: Unified and System Memory.** Separate addressing, placement and access behavior. Actual support depends on the platform.

<https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html>

**S09 — Khronos Group: Vulkan Guide: Synchronization.** Execution and memory synchronization concepts; consult the selected API specification for implementation.

<https://docs.vulkan.org/guide/latest/synchronization.html>

**S10 — Samuel Williams, Andrew Waterman and David Patterson / UC Berkeley: Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures, technical report EECS-2008-134.** Original performance-model reference. All numerical worksheet examples in this package are original hypothetical values.

<https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.html>

**S11 — Python Software Foundation: timeit — Measure execution time of small code snippets.** Timing boundaries and repeated experiments. Package execution was tested on Python 3.13.5, not every documented version.

<https://docs.python.org/3/library/timeit.html>

**S12 — Android Developers: Android Dynamic Performance Framework.** Device-dependent thermal and performance-management context; physical use remains optional.

<https://developer.android.com/games/optimize/adpf>

**S13 — SDL Project: SDL3: SDL_Event.** Event representation and timestamps. An event timestamp is not a photon measurement.

<https://wiki.libsdl.org/SDL3/SDL_Event>

**S14 — Android Developers: Frame Pacing library.** Presentation and frame-pacing context. The supplied trace is synthetic, not captured by this library.

<https://developer.android.com/games/sdk/frame-pacing>

**S15 — Android Developers: The activity lifecycle.** Lifecycle and state-management context. The teaching state machine intentionally simplifies operating-system behavior.

<https://developer.android.com/guide/components/activities/activity-lifecycle>

**S16 — Khronos Group: OpenXR 1.1 reference: xrWaitFrame.** Frame timing contract. No real XR runtime was executed for this package.

<https://registry.khronos.org/OpenXR/specs/1.1/man/html/xrWaitFrame.html>

**S17 — Khronos Group: OpenXR 1.1 reference: xrLocateViews.** Space-, time- and view-dependent pose information.

<https://registry.khronos.org/OpenXR/specs/1.1/man/html/xrLocateViews.html>

**S18 — Cornell University: ECE 5745: Complex Digital ASIC Design.** Deeper digital-design and evaluation study. This package is not a substitute for an ASIC implementation flow.

<https://www.csl.cornell.edu/courses/ece5745/>

**S19 — gem5 Project: gem5 documentation.** Supported architectural simulation as an optional deeper path; gem5 is not a required dependency.

<https://www.gem5.org/documentation/>

**S21 — Apple Developer: Synchronizing CPU and GPU work.** A platform-specific synchronization reference; the documentation page may require JavaScript.

<https://developer.apple.com/documentation/metal/synchronizing-cpu-and-gpu-work>

## Original assigned-reading directory
The following R-codes are used by this volume or its review prerequisites. Their wording and URLs are retained from the original program directory; inclusion is an assigned-study pointer, not a claim that every linked external resource was reread in full for this edition. The full original directory remains in the JSON source.

**R09 — MIT OpenCourseWare: 18.05 Introduction to Probability and Statistics.** Probability, inference and quantitative reasoning.

<https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/>

**R11 — C++ Core Guidelines editors: C++ Core Guidelines.** Resource safety, interfaces, classes and concurrency; guidance rather than the normative language standard.

<https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>

**R21 — Khronos Group: Vulkan tutorial.** Explicit graphics API study; feature-check the device before using the moving latest tutorial.

<https://docs.vulkan.org/tutorial/latest/00_Introduction.html>

**R22 — SDL project: SDL3 documentation.** Windowing, input, audio and platform services; do not mix SDL2 and SDL3 examples.

<https://wiki.libsdl.org/SDL3/FrontPage>

**R23 — Matt Pharr, Wenzel Jakob, Greg Humphreys: Physically Based Rendering, fourth edition.** Rendering mathematics and implementation; use chapter titles in lesson assignments.

<https://www.pbr-book.org/4ed/contents>

**R24 — Microsoft: Direct3D 12 graphics.** Windows graphics backend reference.

<https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-graphics>

**R25 — Apple: Metal developer resources.** Apple-platform graphics and compute reference.

<https://developer.apple.com/metal/>

**R26 — Epic Games: Programming with C++ in Unreal Engine.** Engine comparison after C++ foundations, not a beginner substitute.

<https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine>

**R29 — Microsoft: Xbox Accessibility Guidelines.** Accessibility design and testing; not a legal-compliance certificate.

<https://learn.microsoft.com/en-us/xbox/accessibility/guidelines>

**R30 — MIT OpenCourseWare: 6.002 Circuits and Electronics.** Circuits, transistors and laboratory reasoning.

<https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/>

**R33 — YosysHQ: Yosys documentation.** Synthesis and technology mapping; stable installed release preferred over a development snapshot.

<https://yosyshq.readthedocs.io/projects/yosys/en/latest/>

**R36 — KiCad project: KiCad documentation.** Schematic capture, PCB layout and manufacturing outputs.

<https://docs.kicad.org/>

**R37 — NVIDIA: CUDA Programming Guide.** GPU execution and memory; CUDA is an optional vendor-specific lab route.

<https://docs.nvidia.com/cuda/cuda-programming-guide/>

**R38 — gem5 project: gem5 documentation.** Architecture simulation; distinguish model outputs from measured hardware results.

<https://www.gem5.org/documentation/>

**R43 — Samuel Williams, Andrew Waterman and David Patterson: Roofline performance model, technical report.** Original 2008 performance-model reference; use current measured hardware limits for experiments.

<https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.html>

**R48 — MIT OpenCourseWare: 6.823 Computer System Architecture.** Graduate architecture foundations; historical course concepts supplemented with current specifications.

<https://ocw.mit.edu/courses/6-823-computer-system-architecture-fall-2005/>

**R49 — Christopher Batten / Cornell University: ECE5745 Complex Digital ASIC Design.** Graduate ASIC methodology, circuits, EDA and design-project expectations.

<https://www.csl.cornell.edu/courses/ece5745/>

**R51 — Linux kernel contributors: Driver implementer API guide.** Device ownership, I/O, DMA and driver interfaces; use disposable VMs or simulated devices for kernel experiments.

<https://docs.kernel.org/driver-api/index.html>

**R52 — Khronos Group: OpenXR registry and specifications.** XR coordinate spaces, frame timing and runtime interfaces; optional hardware-dependent extension.

<https://registry.khronos.org/OpenXR/>

**R53 — Zephyr Project: Zephyr documentation.** Embedded kernel, drivers, board support and simulation; select and pin a supported release.

<https://docs.zephyrproject.org/latest/introduction/index.html>
