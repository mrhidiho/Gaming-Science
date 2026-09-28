# Worked demonstration for Lesson 02.1.
count_text = "3"
price_text = "4"
print("text addition:", count_text + price_text)
try:
    count = int(count_text)
    price = int(price_text)
    if count < 0 or price < 0:
        raise ValueError("count and price must be nonnegative")
    print("numeric cost:", count * price)
except ValueError as error:
    print("Input rejected:", error)
