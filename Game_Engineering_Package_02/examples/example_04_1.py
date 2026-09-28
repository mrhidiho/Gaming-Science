# Worked demonstration for Lesson 04.1.
def buggy_damage(health, damage):
    health = max(0, health - damage)
    health = max(0, health - damage)  # Deliberate duplicate update.
    return health

starting_health = 10
one_hit = 3
expected_health = 7
actual_health = buggy_damage(starting_health, one_hit)
print("expected:", expected_health)
print("actual:", actual_health)
print("defect observed:", actual_health != expected_health)
