#Task 4: Square
def square(number):
    return number*number
number = int(input("Please enter your number: "))
print(square(number))

#Task 5: Exponent and Default Exponent
base = float(input("Enter your  base number: "))
exp = (input("Enter your exponent or press enter for default exponent: "))

def power(base,exp):
    return base**exp

if exp == "":
    exp=2
else:
    exp = int(exp)
print(power(base,exp))

