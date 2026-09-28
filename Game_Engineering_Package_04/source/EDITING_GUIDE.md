# Editable source guide

LESSONS.json stores the canonical lesson data, original three-question quizzes and the two added questions. The original quiz_question_count field remains3 for continuity; expanded_quiz_question_count is5. ORIGINAL_VOLUME_03_MANIFEST.json preserves the original module/lesson contracts. PRACTICE.json contains the added exercises, reviews, project elaborations and transfer-review guidance.

The Markdown files are editable text editions of the PDFs. COURSE.html is a self-contained prebuilt reader; COURSE_STYLE.css and COURSE_PROGRESS.js are its stylesheet and interaction source. PDF_STYLE.css records the print typography. Editing a Markdown or JSON file does not automatically update the prebuilt PDFs or reader. Regenerate those outputs through an appropriate Markdown/HTML-to-PDF workflow and recheck layout and assessments after edits.

Code has no external library dependencies beyond the selected C/C++ standard libraries. Optional helper scripts use the Python standard library. Document regeneration is separate from learning/building the C++ examples and may require additional authoring tools. No font files are distributed.

The starter contracts are deliberately smaller than the full labs and are not all drop-in signatures for the reference support library. Compare documented behavior and ownership rules rather than blindly copying class declarations. Keep module and lesson IDs stable when adding exercises.
