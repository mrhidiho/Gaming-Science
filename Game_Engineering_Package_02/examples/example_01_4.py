# Worked demonstration for Lesson 01.4.
speed_units_per_second = 6.0
dt_milliseconds = 250.0
dt_seconds = dt_milliseconds / 1000.0
travel_units = speed_units_per_second * dt_seconds
print("travel units:", travel_units)

frames_per_second = 120
interval_ms = 1000.0 / frames_per_second
print("target interval ms:", round(interval_ms, 3))
