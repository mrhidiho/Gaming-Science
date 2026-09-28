def simulate_resources(turns):
    """Start at zero; each turn collect 3, then spend 5 if affordable.

    Return initial state followed by one resource count per turn.
    """
    if type(turns) is not int or turns < 0:
        raise ValueError("turns must be a nonnegative integer")
    resources = 0
    trace = [resources]
    for _ in range(turns):
        resources += 3
        if resources >= 5:
            resources -= 5
        trace.append(resources)
    return trace
