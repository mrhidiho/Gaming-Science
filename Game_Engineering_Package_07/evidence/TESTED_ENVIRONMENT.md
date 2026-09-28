# Tested environment

Package reference checks executed September 28, 2026. These are supplied-code checks, not learner capstone results.

**python:** 3.13.5 (main, Jul 15 2026, 20:25:40) [GCC 14.2.0]

**platform:** Linux-6.18.44-x86_64-with-glibc2.41

**machine:** x86_64

**g++:** g++ (Debian 14.2.0-19) 14.2.0

**cmake:** cmake version 3.31.6

**chromium:** Chromium 144.0.7559.96 built on Debian GNU/Linux 13 (trixie)

## Executed checks

98 reference contract cases across 20 lessons; 17 invariant/oracle test methods (including 700 seeded randomized cases across six methods); all 20 demonstrations; all five Python integration companions; native C++17 build/CTest; and an AddressSanitizer + UndefinedBehaviorSanitizer run of the native offline harness.

The audio harness tested 100 paired blocks, sample bounds, ring empty/full/FIFO/wrap and invalid-command handling. The queue test was single-threaded. No actual audio device was opened and no deadline/underrun measurement was claimed.

The browser UI was tested using direct document-content rendering in system Chromium, because the container browser’s administrative policy blocked both file and loopback HTTP navigation. Search, answer reveal, score/checkbox state, progress export/import, invalid-import rejection, confirmed reset, storage-unavailable handling and a 390-pixel viewport were exercised. Native local-storage persistence and link navigation were not verified. This is not a human accessibility review or an all-browser certificate.

PDFs were generated programmatically with ReportLab. Representative cover, contents, lesson, workbook, answer, reference and rubric pages were rasterized and visually inspected. Text bounds were checked programmatically on every page. PDF review does not establish screen-reader tagging or PDF/UA compliance.

## Not executed / learner work

The learner’s engine and game; the maintained physics-library comparison; platform audio/device stress; concurrent queue stress; real process/socket multiplayer; a complete match registry/production identity adapter; target-machine frame/inference measurements; power-loss durability; other operating systems; human usability/accessibility tasks; and independent Gate F review remain unperformed here. See the full lab cards and templates.

The Python baseline is 3.11+ syntax; actual execution used the version above. The native baseline is C++17. Other versions and operating systems are not labeled as separately tested.
