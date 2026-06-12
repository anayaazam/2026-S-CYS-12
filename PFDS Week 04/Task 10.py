#Task 10: Calculator
def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    return a/b
a = float(input("Please enter your first number: "))
b = float(input("Please enter your second number: "))
operator = str(input("Please enter your operator: "))
if operator == "+":
    print(add(a,b))
elif operator == "-":
    print(sub(a,b))
elif operator == "*":
        print(mul(a,b))
elif operator == "/":
        print(div(a,b))
else:
    print("Operator is not correct")
