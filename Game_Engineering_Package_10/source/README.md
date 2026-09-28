# Editable curriculum sources

`original_volume09.json` preserves the source curriculum's five modules and 20 lesson records. `curriculum_expanded.json` preserves every original lesson field and adds an `expansion` object for new sections, worked examples, procedures, checks, two problems and two solutions. Original quiz IDs/order remain tied to each lesson. `references.json` preserves the R-series IDs and adds the S-series focused readings.

The Markdown files are the editable print-source snapshots for the six main documents and five standalone modules. `browser.js` and `browser.css` are the editable browser behavior/style snapshots embedded in `COURSE.html`. The HTML is self-contained; it does not fetch these source files at runtime. Editing one representation does not automatically update the other representations. Preserve lesson IDs and validate all cross-references when regenerating a format with your preferred publishing tools.

The book's original quiz answers appear in the separate key and JSON source; the student PDF does not print them after the questions. Browser answer panels are closed initially. This is a learning workflow, not a secured exam system.

Python/C++ teaching references under `code` do not require document-generation dependencies. External full texts and font files are not bundled. Printed reference URLs and source status are available in REFERENCE_GUIDE.pdf.
