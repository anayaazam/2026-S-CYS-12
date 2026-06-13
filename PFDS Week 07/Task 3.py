# Task 3: Nested loop
for i in range(1, 3):
    for j in range(1, 3):
        print("i=", i, "j=", j)

# Task 4: Triangle and Quad pattern
for i in range(1, 5):
    for j in range(5):
        print("*", end=" ")
    print()

print("\n")
for i in range(1, 5):
    for j in range(i):
        print("*", end=" ")
    print()

# Task 5: Dictionaries
fruits = {"apple": "sayb", "banana": "kayla", "mango": "aam"}
print(fruits)
print(fruits["banana"])
print(fruits["apple"])
print(fruits["mango"])

