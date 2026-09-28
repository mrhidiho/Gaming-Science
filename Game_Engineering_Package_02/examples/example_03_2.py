# Worked demonstration for Lesson 03.2.
def spend(resources, cost):
    if resources < 0 or cost < 0:
        raise ValueError("nonnegative amounts required")
    if cost > resources:
        return resources
    return resources - cost

def main():
    resources = 8
    for cost in (5, 5, 0):
        resources = spend(resources, cost)
        print("cost:", cost, "remaining:", resources)

if __name__ == "__main__":
    main()
