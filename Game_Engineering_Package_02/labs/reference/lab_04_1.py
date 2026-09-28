def apply_damage(health, damage):
    """Apply one nonnegative integer damage event; health cannot fall below zero."""
    if (type(health) is not int or type(damage) is not int
            or health < 0 or damage < 0):
        raise ValueError("health and damage must be nonnegative integers")
    return max(0, health - damage)
