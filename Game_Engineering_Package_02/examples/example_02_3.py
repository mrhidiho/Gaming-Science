# Worked demonstration for Lesson 02.3.
resources = 0
print("initial:", resources)
for turn in range(1, 6):
    resources = resources + 3
    if resources >= 5:
        resources = resources - 5
    print("turn", turn, "resources", resources)
