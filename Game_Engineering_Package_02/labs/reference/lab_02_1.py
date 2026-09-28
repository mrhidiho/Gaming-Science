def total_cost(count_text, unit_cost_text):
    """Convert whole-number text; reject negative quantities and bad text."""
    try:
        count = int(count_text)
        unit_cost = int(unit_cost_text)
    except (ValueError, TypeError) as exc:
        raise ValueError("enter whole-number count and price") from exc
    if count < 0 or unit_cost < 0:
        raise ValueError("count and price must be nonnegative")
    return count * unit_cost
