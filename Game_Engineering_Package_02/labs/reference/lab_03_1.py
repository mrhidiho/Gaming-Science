def index_units(units):
    """Flat unit records with id/name/health; duplicate IDs are rejected.

    Return a dictionary of independent shallow record copies.
    """
    result = {}
    for unit in units:
        identifier = unit["id"]
        if identifier in result:
            raise ValueError("duplicate unit ID")
        result[identifier] = dict(unit)
    return result

def living_units(units):
    """Return new flat-record copies for units with health > 0."""
    return [dict(unit) for unit in units if unit["health"] > 0]
