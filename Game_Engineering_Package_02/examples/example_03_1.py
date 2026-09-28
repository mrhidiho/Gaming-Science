# Worked demonstration for Lesson 03.1.
units = [
    {"id": 101, "name": "Scout", "health": 8},
    {"id": 102, "name": "Scout", "health": 0},
]
alias = units
copies = [dict(unit) for unit in units]
alias[0]["name"] = "Runner"
copies[0]["name"] = "Independent"
print("original name:", units[0]["name"])
print("copied name:", copies[0]["name"])
print("living IDs:", [unit["id"] for unit in units if unit["health"] > 0])
