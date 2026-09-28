# Edition validation and limits

Prepared September 28, 2026.

## Document structure

Verified 50 modules, 200 unique lesson IDs, 600 questions and 600 explanatory answers. Every lesson has an objective, teaching text, example, practical task, assigned study and quiz. The main PDF has 299 pages and 304 outline entries. The answer key has 52 pages. Each separate volume has 27 pages. The main PDF repeats the first two lessons in the Start Here section for convenience; this does not increase the count of unique lessons.

All pages of the main PDF and answer key were rendered with PDFium. Contact sheets and representative full-size pages were inspected. Automated text-boundary and missing-quiz checks found no issues. This is document-layout and structural validation, not independent academic peer review.

## Starter programs

Python: 23 unittest methods passed, with additional parameterized cases. C++: configured and compiled, with the CTest motion-contract target passing. Python and C++ motion-demo output matched. Exact tested environment is in starter/TESTED_ENVIRONMENT.md. These checks cover the provided starter code, not the learner's future implementations.

## Browser edition

The authored HTML and JavaScript were exercised in Chromium. Checks passed for all 200 lesson panels, closed-by-default answers, lesson search and clearing, progress changes, export/import, and the storage-unavailable fallback. Mobile-width layout had no horizontal page overflow. No JavaScript errors were observed.

The QA browser's managed navigation policy prevented file-origin and localhost navigation. The interface was tested by loading the authored markup directly. Persistence across file-origin browser sessions was therefore not validated in that environment. Export progress backups regularly; storage behavior varies by browser and file location.

## Academic and platform limitations

This is an original guided curriculum, not an accredited program or a guarantee of a degree-level outcome. Graduate work should receive qualified independent review. Assigned readings, problem sets, implementations, project defenses and research are essential parts of the course. External references are linked rather than copied, and their versions may change.
