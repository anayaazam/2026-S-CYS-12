def count_words(text):
    count = 0
    for word in text.split():
        count += 1
    return count
def count_characters(text):
    count = 0
    for char in text:
        count += 1
    return count
def count_spaces(text):
    count = 0
    for char in text:
        if char == " ":
            count += 1
    return count
def count_commas(text):
    count = 0
    for char in text:
        if char == ",":
            count += 1
    return count
def count_periods(text):
    count = 0
    for char in text:
        if char == ".":
            count += 1
    return count
def count_sentences(text):
    count = 0
    for char in text:
        if char in ".!?":
            count += 1
    return count
def count_vowels(text):
    count = 0
    for char in text:
        if char.lower() in "aeiou":
            count += 1
    return count
def count_digits(text):
    count = 0
    for char in text:
        if char.isdigit():
            count += 1
    return count
def count_uppercase(text):
    count = 0
    for char in text:
        if char.isupper():
            count += 1
    return count
def count_lowercase(text):
    count = 0
    for char in text:
        if char.islower():
            count += 1
    return count
def count_special(text):
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\`~"
    count = 0
    for char in text:
        if char in special_characters:
            count += 1
    return count
print("Paste your paragraph below.")
print("When you are done, type END on a new line and press Enter.\n")
lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        text = "\n".join(lines)
        word_count = count_words(text)
        if word_count >= 700:
            break
        elif word_count < 700:
            print(f"\nNote: Atleast 700 words are required.\n")
    else:
        lines.append(line)
print("Results:")
print(f"Words             : {count_words(text)}")
print(f"Characters        : {count_characters(text)}")
print(f"Spaces            : {count_spaces(text)}")
print(f"Commas            : {count_commas(text)}")
print(f"Periods           : {count_periods(text)}")
print(f"Sentences         : {count_sentences(text)}")
print(f"Vowels            : {count_vowels(text)}")
print(f"Digits            : {count_digits(text)}")
print(f"Uppercase letters : {count_uppercase(text)}")
print(f"Lowercase letters : {count_lowercase(text)}")
print(f"Special characters: {count_special(text)}")
