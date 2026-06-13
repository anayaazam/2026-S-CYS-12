# GENERAL  LAMBDA FUNCTIONS

# Example 1: Simple addition
add = lambda x, y: x + y
print(add(5, 3))


# Example 2: Square a number
square = lambda x: x ** 2
print(square(4))


# Example 3: Check if number is even
is_even = lambda x: x % 2 == 0
print(is_even(7))
print(is_even(10))


# Example 4: Convert to uppercase
to_upper = lambda s: s.upper()
print(to_upper("hello"))


# Example 5: Find maximum of two numbers
max_num = lambda a, b: a if a > b else b
print(max_num(15, 20))


# Example 6: Calculate area of rectangle
area = lambda l, w: l * w
print(area(5, 4))


# Example 7: Get first character
first_char = lambda s: s[0] if s else ''
print(first_char("Python"))


# Example 8: Reverse a string
reverse = lambda s: s[::-1]
print(reverse("hello"))


# Example 9: Check if string starts with vowel
starts_with_vowel = lambda s: s[0].lower() in 'aeiou'
print(starts_with_vowel("apple"))
print(starts_with_vowel("banana"))


# Example 10: Convert Celsius to Fahrenheit
c_to_f = lambda c: (c * 9/5) + 32
print(c_to_f(0))
print(c_to_f(100))



# LAMBDA + MAP

# Example 1: Square all numbers in a list
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)


# Example 2: Convert list of temperatures from Celsius to Fahrenheit
celsius = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print(fahrenheit)


# Example 3: Get length of each string in a list
words = ["Python", "Java", "C++", "JavaScript"]
lengths = list(map(lambda w: len(w), words))
print(lengths)


# Example 4: Add corresponding elements from two lists
list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8]
sums = list(map(lambda x, y: x + y, list1, list2))
print(sums)


# Example 5: Format numbers as currency
prices = [10.5, 20.75, 30.0, 45.99]
formatted = list(map(lambda p: f"${p:.2f}", prices))
print(formatted)



# LAMBDA + FILTER

# Example 1: Filter even numbers from a list
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)


# Example 2: Filter words longer than 5 characters
words = ["cat", "elephant", "dog", "giraffe", "bird", "butterfly"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)


# Example 3: Filter numbers greater than 10
numbers = [5, 12, 8, 15, 3, 20, 7]
greater_than_10 = list(filter(lambda x: x > 10, numbers))
print(greater_than_10)


# Example 4: Filter strings that start with 'A' or 'a'
names = ["Alice", "Bob", "Charlie", "Amanda", "David", "Alex"]
a_names = list(filter(lambda n: n[0].lower() == 'a', names))
print(a_names)


# Example 5: Filter prime numbers from a list
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
primes = list(filter(lambda x: is_prime(x), numbers))
print(primes)



# LAMBDA + SORT

# Example 1: Sort by string length
words = ["python", "java", "c", "javascript", "go", "rust"]
sorted_by_length = sorted(words, key=lambda x: len(x))
print(sorted_by_length)  


# Example 2: Sort by last character of string
names = ["Alice", "Bob", "Charlie", "David", "Eve"]
sorted_by_last_char = sorted(names, key=lambda x: x[-1])
print(sorted_by_last_char) 


# Example 3: Sort list of tuples by second element
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("David", 88)]
sorted_by_grade = sorted(students, key=lambda x: x[1], reverse=True)
print(sorted_by_grade)  


# Example 4: Sort by absolute value
numbers = [-5, 2, -10, 3, -1, 7]
sorted_by_abs = sorted(numbers, key=lambda x: abs(x))
print(sorted_by_abs) 


# Example 5: Sort dictionary by value
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 88}
sorted_by_value = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
print(sorted_by_value) 



# LAMBDA + REDUCE

from functools import reduce
# Example 1: Find product of all numbers
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
print(product)


# Example 2: Find maximum number in a list
numbers = [23, 45, 12, 67, 34, 89, 5]
max_num = reduce(lambda x, y: x if x > y else y, numbers)
print(max_num)


# Example 3: Concatenate all strings in a list
words = ["Python", " ", "is", " ", "awesome", "!"]
sentence = reduce(lambda x, y: x + y, words)
print(sentence)


# Example 4: Count total characters in all strings
words = ["hello", "world", "python", "programming"]
total_chars = reduce(lambda x, y: x + len(y), words, 0)
print(total_chars)


# Example 5: Find the sum of squares of all numbers
numbers = [1, 2, 3, 4, 5]
sum_of_squares = reduce(lambda x, y: x + (y ** 2), numbers, 0)
print(sum_of_squares)















