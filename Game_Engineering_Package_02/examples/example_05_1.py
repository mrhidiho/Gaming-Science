# Worked demonstration for Lesson 05.1.
position = (1, 1)
command = " D ".strip().lower()
deltas = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
dx, dy = deltas[command]
candidate = (position[0] + dx, position[1] + dy)
if 0 <= candidate[0] < 3 and 0 <= candidate[1] < 3:
    position = candidate
for y in range(3):
    row = ""
    for x in range(3):
        row += "P" if (x, y) == position else (
            "E" if (x, y) == (2, 2) else ".")
    print(row)
print("position after drawing:", position)
