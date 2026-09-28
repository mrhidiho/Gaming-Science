"""Day 1: predict each position, run the program, then change one value."""

position_units = 0.0
speed_units_per_second = 6.0
timestep_seconds = 0.25

for tick in range(1, 6):
    position_units = position_units + speed_units_per_second * timestep_seconds
    print(f"tick {tick}: x={position_units:.2f} units")
