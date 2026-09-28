# Sources and provenance

## How this edition relates to the roadmap

Package 06 expands Volume 05 of the September 28, 2026 Computer Science and Computer Engineering for Games manifest. The source manifest and original curriculum were inspected directly. Module/lesson IDs, titles, learning outcomes, original lab assignments, original reading assignments and the first three lesson quiz questions are retained. The additional teaching, worked derivations, procedures, two application questions per lesson, module reviews and code in this bundle are original additions.

The canonical lesson questions were transcribed from the original curriculum PDF's Volume 05 section, not inferred from the shorter manifest. Original assessment examples are retained where a question refers to an example. Answer explanations are expanded. The complete original program and textbooks are not repackaged here.

Reading IDs R11 and R19-R27/R37 retain their original program meanings. S01-S16 are supplementary references for this volume only. Technical source links below were consulted or retrieved on September 28, 2026; S10 is specifically marked as a link-level check. API documentation can change. Record the version actually used in your own lab; this edition does not certify any unspecified browser, SDK, driver or engine release.

## Canonical assigned references

### R11 — C++ Core Guidelines editors: C++ Core Guidelines

Resource safety, interfaces, classes and concurrency; guidance rather than the normative language standard.

<https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>

### R19 — Carnegie Mellon University: 15-462/662 Computer Graphics

Rendering, geometry and animation course structure and exercises.

<https://15462.courses.cs.cmu.edu/fall2021/>

### R20 — Carnegie Mellon University: 15-466/666 Computer Game Programming

Runtime systems and game-production programming.

<https://graphics.cs.cmu.edu/courses/15-466/>

### R21 — Khronos Group: Vulkan tutorial

Explicit graphics API study; feature-check the device before using the moving latest tutorial.

<https://docs.vulkan.org/tutorial/latest/00_Introduction.html>

### R22 — SDL project: SDL3 documentation

Windowing, input, audio and platform services; do not mix SDL2 and SDL3 examples.

<https://wiki.libsdl.org/SDL3/FrontPage>

### R23 — Matt Pharr, Wenzel Jakob, Greg Humphreys: Physically Based Rendering, fourth edition

Rendering mathematics and implementation; use chapter titles in lesson assignments.

<https://www.pbr-book.org/4ed/contents>

### R24 — Microsoft: Direct3D 12 graphics

Windows graphics backend reference.

<https://learn.microsoft.com/en-us/windows/win32/direct3d12/direct3d-12-graphics>

### R25 — Apple: Metal developer resources

Apple-platform graphics and compute reference.

<https://developer.apple.com/metal/>

### R26 — Epic Games: Programming with C++ in Unreal Engine

Engine comparison after C++ foundations, not a beginner substitute.

<https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine>

### R27 — Glenn Fiedler: Fix Your Timestep!

Original practitioner explanation of fixed-step simulation; read critically and implement your own lab.

<https://gafferongames.com/post/fix_your_timestep/>

### R37 — NVIDIA: CUDA Programming Guide

GPU execution and memory; CUDA is an optional vendor-specific lab route.

<https://docs.nvidia.com/cuda/cuda-programming-guide/>

## Supplemental primary sources

### S01 — W3C: WebGPU Shading Language (WGSL)

Host-shareable layout, alignment, storage/uniform contracts; evolving specification.

<https://www.w3.org/TR/WGSL/>

### S02 — Netpbm: PPM format specification

Strict PPM and the explicitly documented sRGB variant used in this package.

<https://netpbm.sourceforge.net/doc/ppm.html>

### S03 — Khronos Group: glTF 2.0 specification

Material/color semantics and tangent handedness; glTF importing is assigned, not implemented here.

<https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html>

### S04 — Pharr, Jakob and Humphreys: PBRT 4: Bounding Volume Hierarchies

Spatial bounds, construction and traversal.

<https://www.pbr-book.org/4ed/Primitives_and_Intersection_Acceleration/Bounding_Volume_Hierarchies>

### S05 — Khronos Group: Vulkan Tutorial: Frames in flight

Frame contexts; distinguish frame indexing from presentation-image indexing.

<https://docs.vulkan.org/tutorial/latest/03_Drawing_a_triangle/03_Drawing/03_Frames_in_flight.html>

### S06 — GPU for the Web Community Group: WebGPU explainer

Conceptual API overview; an explainer, not a substitute for the normative specification.

<https://gpuweb.github.io/gpuweb/explainer/>

### S07 — Khronos Group: Vulkan Guide: Synchronization examples

Dependencies, stages, accesses and barriers.

<https://docs.vulkan.org/guide/latest/synchronization_examples.html>

### S08 — Khronos Group: Vulkan Guide: Swapchain semaphore reuse

Presentation waits may outlive the graphics submission fence.

<https://docs.vulkan.org/guide/latest/swapchain_semaphore_reuse.html>

### S09 — Microsoft: Using resource barriers in Direct3D 12

Resource state and hazard management; do not transliterate Vulkan flags.

<https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12>

### S10 — Apple: Synchronizing CPU and GPU work

Official Metal starting point. URL retrieved; dynamic page body was not fully inspectable during authoring.

<https://developer.apple.com/documentation/metal/synchronizing-cpu-and-gpu-work>

### S11 — SDL: SDL_GetWindowSizeInPixels

Drawable pixel extent can differ from logical window size.

<https://wiki.libsdl.org/SDL3/SDL_GetWindowSizeInPixels>

### S12 — Khronos Group: Vulkan Tutorial: Swap chain recreation

Out-of-date/zero-extent paths and safe fence-reset sequencing.

<https://docs.vulkan.org/tutorial/latest/03_Drawing_a_triangle/04_Swap_chain_recreation.html>

### S13 — Pharr, Jakob and Humphreys: PBRT 4: Radiometry

Radiometric quantities and their domains.

<https://www.pbr-book.org/4ed/Radiometry,_Spectra,_and_Color/Radiometry>

### S14 — Pharr, Jakob and Humphreys: PBRT 4: Roughness using microfacet theory

Microfacet distributions and model assumptions.

<https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory>

### S15 — Pharr, Jakob and Humphreys: PBRT 4: Image texture

Texture reconstruction, footprints and filtering.

<https://www.pbr-book.org/4ed/Textures_and_Materials/Image_Texture>

### S16 — GPU for the Web Community Group: WebGPU samples

Optional companion examples; no external sample source is bundled.

<https://webgpu.github.io/webgpu-samples/>

## Scope of evidence

The diagrams in this edition are numerical reference-renderer outputs, not external photographs or a claim of hardware-rendered results. All included mesh, image and world fixtures are original procedural teaching data; assets/source/PROVENANCE.md documents them. Code is original and standard-library based except for the platform APIs explicitly used in the optional browser bridge. No textbook chapters, proprietary SDK binaries, third-party game assets or font files are redistributed.

The small examples illustrate contracts, not all details of their parent fields. PBRT supplies deeper transport/acceleration study; platform documentation supplies exact native API rules. The course's broader undergraduate-to-graduate pathway remains self-study, not accreditation, a degree, or a guarantee of employment.
