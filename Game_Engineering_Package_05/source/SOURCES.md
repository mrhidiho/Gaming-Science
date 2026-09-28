# Sources and provenance



The original lesson IDs, titles, outcomes, primers, examples, lab briefs, reading assignments and three-question quizzes come from the supplied `curriculum.json`, edition 2026-09-28. They are retained in `source/original_volume_04.json` and the `source` fields of `source/expanded_curriculum.json`. The original file SHA-256 is `21ffde3c0e228c7729933e4e92010295c7a46001fd05c995090ad79dde773a25`.



The expanded explanations, implementation contracts, code, fifty additional exercises, two application questions per lesson, module reviews and ForgeQueue design are newly authored for Package 05. They are not quoted textbook chapters or completed student work. External books and specifications are linked, not bundled in full.



R-identifiers preserve the source program directory. P-identifiers identify primary documentation consulted for this expansion on September 28, 2026. A moving documentation page is not a pin for the installed tool version; the measured validation environment is recorded separately. R37 remains an inherited optional GPU comparison, not a prerequisite for running the CPU labs. P15 is unused.



The source Module 20 prerequisite literally reads “Volumes 01–04.” For sequencing within this volume, this expansion interprets that as the preceding foundations and Modules 16–19 before Module 20, rather than requiring Module 20 to be completed before itself. The source text is retained unchanged in the source data.



## R01 — CS2023 knowledge areas

ACM / IEEE-CS / AAAI

Breadth checklist, not a claim of accreditation.

[Open the primary/source resource](https://csed.acm.org/knowledge-areas/)



## R02 — Computer Engineering Curricula 2016

ACM / IEEE Computer Society

Computer-engineering breadth and laboratory expectations; historical curriculum report.

[Open the primary/source resource](https://ieeecs-media.computer.org/assets/pdf/ce2016-final-report.pdf)



## R04 — Python tutorial and language documentation

Python Software Foundation

Reference companion; the tutorial itself assumes some programming familiarity.

[Open the primary/source resource](https://docs.python.org/3/tutorial/)



## R05 — Pro Git

Scott Chacon and Ben Straub

Version control and collaboration.

[Open the primary/source resource](https://git-scm.com/book/en/v2)



## R11 — C++ Core Guidelines

C++ Core Guidelines editors

Resource safety, interfaces, classes and concurrency; guidance rather than the normative language standard.

[Open the primary/source resource](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)



## R12 — CMake tutorial

Kitware

Build systems; use documentation matching the installed release.

[Open the primary/source resource](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)



## R15 — 6.004 Computation Structures

MIT OpenCourseWare

Logic, processor design, memory and systems.

[Open the primary/source resource](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)



## R16 — Operating Systems: Three Easy Pieces

Remzi and Andrea Arpaci-Dusseau

Virtualization, concurrency and persistence; book by its authors.

[Open the primary/source resource](https://pages.cs.wisc.edu/~remzi/OSTEP/)



## R17 — RFC 9293: Transmission Control Protocol

IETF / RFC Editor

Transport semantics; reference reading after networking foundations.

[Open the primary/source resource](https://www.rfc-editor.org/rfc/rfc9293.html)



## R18 — PostgreSQL tutorial

PostgreSQL Global Development Group

Relational data, transactions and SQL; pin local server and client versions.

[Open the primary/source resource](https://www.postgresql.org/docs/current/tutorial.html)



## R29 — Xbox Accessibility Guidelines

Microsoft

Accessibility design and testing; not a legal-compliance certificate.

[Open the primary/source resource](https://learn.microsoft.com/en-us/xbox/accessibility/guidelines)



## R35 — RISC-V ISA specifications

RISC-V International

Instruction-set reference; record the exact ISA version and implemented extensions.

[Open the primary/source resource](https://docs.riscv.org/reference/isa/)



## R37 — CUDA Programming Guide

NVIDIA

GPU execution and memory; CUDA is an optional vendor-specific lab route.

[Open the primary/source resource](https://docs.nvidia.com/cuda/cuda-programming-guide/)



## P01 — RISC-V ELF psABI: integer register and calling conventions

RISC-V non-ISA specifications project

Use the ILP32 integer convention for the teaching RV32 routine; no floating-point ABI claim.

[Open the primary/source resource](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/)



## P02 — Developer options: optimization reports

GNU Compiler Collection

Match options and interpretation to the installed compiler.

[Open the primary/source resource](https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html)



## P03 — Clang user manual: optimization remarks

LLVM Project

Compiler diagnostic interface, not a performance guarantee.

[Open the primary/source resource](https://clang.llvm.org/docs/UsersManual.html)



## P04 — AddressSanitizer

LLVM Project

Instrumented checks; platform support and observed coverage have limits.

[Open the primary/source resource](https://clang.llvm.org/docs/AddressSanitizer.html)



## P05 — ThreadSanitizer

LLVM Project

Data-race detection; separate from ASan and not a proof of liveness.

[Open the primary/source resource](https://clang.llvm.org/docs/ThreadSanitizer.html)



## P06 — os: replacement and synchronization interfaces

Python Software Foundation

File and directory durability require a platform-specific failure model.

[Open the primary/source resource](https://docs.python.org/3/library/os.html)



## P07 — mmap

Python Software Foundation

Read-only mapping and platform-specific behavior.

[Open the primary/source resource](https://docs.python.org/3/library/mmap.html)



## P08 — subprocess

Python Software Foundation

Argument lists, checked results and timeout behavior for a trusted program.

[Open the primary/source resource](https://docs.python.org/3/library/subprocess.html)



## P09 — socket

Python Software Foundation

Partial reads, socket waits and connection behavior.

[Open the primary/source resource](https://docs.python.org/3/library/socket.html)



## P10 — sqlite3

Python Software Foundation

Connection and transaction handling. Tested runtime is recorded separately.

[Open the primary/source resource](https://docs.python.org/3/library/sqlite3.html)



## P11 — Foreign key support

SQLite project

Explicit per-connection enforcement in the lab.

[Open the primary/source resource](https://sqlite.org/foreignkeys.html)



## P12 — Transactions

SQLite project

BEGIN IMMEDIATE, writer behavior and explicit transactions.

[Open the primary/source resource](https://sqlite.org/lang_transaction.html)



## P13 — CTest command-line reference

Kitware

Use documentation matching the installed CMake/CTest version.

[Open the primary/source resource](https://cmake.org/cmake/help/latest/manual/ctest.1.html)



## P14 — concurrent.futures

Python Software Foundation

Future completion, executor shutdown and cancellation contracts.

[Open the primary/source resource](https://docs.python.org/3/library/concurrent.futures.html)



## P16 — RV32I base integer ISA, version 2.1; library snapshot v20260120

RISC-V International

Pinned specification entry for instruction semantics; no full-ISA emulator is supplied.

[Open the primary/source resource](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html)
