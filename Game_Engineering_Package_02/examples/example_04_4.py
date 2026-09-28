# Worked demonstration for Lesson 04.4.
def proposed_purchase(balance, cost):
    # Deliberate review candidate: inspect the boundary comparison.
    if balance > cost:
        return balance - cost
    return balance

for balance, cost in ((6, 5), (5, 5), (4, 5)):
    print("balance/cost/result:", balance, cost,
          proposed_purchase(balance, cost))
print("Review question: should exact affordability be accepted?")
