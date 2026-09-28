# Worked demonstration for Lesson 05.3.
import hashlib
import json

first = {"x": 9, "y": 9, "won": True}
second = {"won": True, "y": 9, "x": 9}
first_text = json.dumps(first, sort_keys=True, separators=(",", ":"))
second_text = json.dumps(second, sort_keys=True, separators=(",", ":"))
first_digest = hashlib.sha256(first_text.encode("utf-8")).hexdigest()
second_digest = hashlib.sha256(second_text.encode("utf-8")).hexdigest()
print("same canonical text:", first_text == second_text)
print("same digest:", first_digest == second_digest)
print("canonical text:", first_text)
