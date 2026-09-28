# Worked demonstration for Lesson 05.2.
world = {"x": 1, "y": 0, "won": False}
obstacles = {(1, 1), (3, 2), (4, 4), (7, 6), (8, 8)}
candidate = (world["x"], world["y"] + 1)
next_world = dict(world)
if (0 <= candidate[0] < 10 and 0 <= candidate[1] < 10
        and candidate not in obstacles):
    next_world["x"], next_world["y"] = candidate
    next_world["won"] = candidate == (9, 9)
print("attempted cell:", candidate)
print("original:", world)
print("result:", next_world)
