def can_open(has_key, level, stamina):
    """Trusted inputs: bool key and nonnegative integer level/stamina."""
    return has_key or (level >= 5 and stamina >= 10)
