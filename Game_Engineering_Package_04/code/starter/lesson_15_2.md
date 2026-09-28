# Student contract 15.2: Lexing, parsing and syntax trees

Implement tokens, recursive-descent parsing and evaluation for numbers, parentheses and four arithmetic operators. Pass: test precedence, associativity, malformed input, unknown names and division-by-zero policy.

1. Write the grammar, numeric domain, evaluation order and error-location policy before coding.
2. Implement a bounded lexer retaining offsets and a recursive-descent parser producing an arena AST.
3. Implement evaluation with intermediate-range and division checks.
4. Test precedence, associativity, malformed input, unknown names and all declared resource limits.

## Cases

1. 2+3*4 -> 14
2. (2+3)*4 -> 20
3. 8-3-1 -> 4
4. -8/3 -> -2
5. 1/(2-2) -> division error at slash
6. empty/2 3/unknown name -> diagnostic
7. excess source, tokens, nodes or depth rejected

## Evidence

Language specification, token/AST traces, golden-result table, located diagnostics and bounded-input tests.

## Transfer

Add a remainder operator. Specify precedence, negative-operand behavior and zero-divisor policy before changing the lexer or parser.
