def spend(resources, cost):
    """Nonnegative integers; unaffordable spending leaves resources unchanged."""
    if (type(resources) is not int or type(cost) is not int
            or resources < 0 or cost < 0):
        raise ValueError("resources and cost must be nonnegative integers")
    if cost > resources:
        return resources
    return resources - cost
