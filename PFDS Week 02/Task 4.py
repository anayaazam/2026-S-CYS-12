#Task 4: Password Generator
import string
import random
length = int(input("Enter the length of the password:"))

lower=string.ascii_lowercase
upper= string.ascii_uppercase
numbers = string.digits
symbols = string.punctuation
all= lower+upper+numbers+symbols
temp = random.sample(all,length)
password = "".join(temp)
print(password)
