# Worked demonstration for Lesson 04.2.
def bounded_move(position, delta, size):
    candidate = position + delta
    if 0 <= candidate < size:
        return candidate
    return position

cases = [(2, 1, 4, 3), (3, 1, 4, 3), (0, -1, 4, 0)]
for position, delta, size, expected in cases:
    actual = bounded_move(position, delta, size)
    assert actual == expected
print("three independent boundary cases passed")

for position in range(4):
    for delta in (-1, 0, 1):
        assert 0 <= bounded_move(position, delta, 4) < 4
print("twelve bounded-input property cases passed")
