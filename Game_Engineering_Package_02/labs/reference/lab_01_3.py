def swap_values(a, b):
    """Return the two input values in reversed order."""
    temporary = a
    a = b
    b = temporary
    return a, b
