# Worked demonstration for Lesson 02.2.
cases = [(False, 4, 10), (False, 5, 10), (True, 1, 0)]
for has_key, level, stamina in cases:
    allowed = has_key or (level >= 5 and stamina >= 10)
    print(has_key, level, stamina, "->", allowed)
