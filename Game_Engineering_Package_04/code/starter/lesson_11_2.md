# Student contract 11.2: Integer, floating-point and object representations

Print relevant sizes and numeric limits on the available compiler. Write checked conversions for a file length and tests for boundary values. Pass: do not trigger signed overflow as a test oracle; reject out-of-range input before converting.

1. Print numeric limits, sizes, byte width and selected alignment values. Mark which are observations rather than portable constants.
2. Implement checked decimal length parsing and pre-multiplication budget checks.
3. Write a field-based little-endian encoder/decoder and compare with independently written bytes.
4. Test numeric boundaries and document the difference between Python integers and the chosen native representation.

## Cases

1. 0 and exact application maximum accepted
2. negative text and trailing junk rejected
3. one above the application limit rejected
4. huge decimal value rejected by parser
5. 42 records of 24 bytes accepted under 1024; 43 rejected
6. 0x12345678 encodes to 78 56 34 12

## Evidence

Representation report, boundary-test table, checked conversion implementation, specified encoding and a comparison with the earlier Python model.

## Transfer

A texture claims width = 100,000 and height = 100,000. Design checks for width * height * bytes_per_pixel without overflowing during validation.
