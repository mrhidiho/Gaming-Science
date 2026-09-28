# Student contract 11.4: Standard containers, iterators and error handling

Port the unit list to std::vector and implement lookup with an explicit not-found result. Pass: test empty input, missing ID and growth; document which operations invalidate stored references.

1. Port the unit list to a vector-backed API with unique IDs and copied optional lookup results.
2. Test empty, present and missing queries, duplicate insertion, growth and erasure.
3. Write an invalidation table for reserve, append, erase and clear. Include the past-the-end iterator.
4. Classify normal absence, bad external input and invariant failure; explain the chosen error channel for each.

## Cases

1. empty lookup -> absent
2. duplicate ID -> rejected with unchanged size
3. growth preserves logical ID lookup
4. missing removal -> false and unchanged state
5. erase adjacent zero-HP units correctly
6. reserve changes capacity, not constructed count

## Evidence

Unit repository, automated tests, error taxonomy and operation-specific invalidation table.

## Transfer

A renderer stores vector iterators across an update that removes dead units. Redesign the frame boundary so rendering never uses invalid iterators.
