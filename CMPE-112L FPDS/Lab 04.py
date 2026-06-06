#Task 1: UDF Greet Function
def greet(hello):
    return hello("Welcome to Python Programming")
status= str(input("Please enter your learning status: 'Beginner' or 'Experienced'"))
if status == "Beginner" or status == "beginner":
    greet(print)
elif status == "Experienced" or status == "experienced":
    greet(print)
else:
    greet(print)



#Task 2: Name Function
def hello(name):
    return ("Hello," + name)
name = str(input("Please enter your name: "))
print(hello(name))



#Task 3: Add a and b
def add(a,b):
    return a+b
a=float(input("Please enter your first number: "))
b=float(input("Please enter your second number: "))
print(add(a,b))



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



#Task 6: Student(name,age)
name= input("Please enter your name: ")
age= input("Please enter your age: ")
def student(name,age):
    return 'The name of the student is',name,'and their age is',age
print(student(name,age))



#Task 7: Maximum
a=float(input("Please enter your first number: "))
b=float(input("Please enter your second number: "))
c=float(input("Please enter your third number: "))

def compare(a,b,c):
    return max(a,b,c)
max=  max(a,b,c)
print("The largest number is ",max)



#Task 8: Total(*numbers)
#variable length arguments
def sum_all(*args):
    return sum(args)
print (sum_all(1,2,3,4,5,6,7,8,9))
print (sum_all(193,345))
print(sum_all(112,366,864,345,234,456,567))
print (sum_all(26,36,67,38,95,85,54,65,63,32,52))




#Task 9: Average(*numbers)
sum=0
inputs= int(input("Please enter your number of inputs: "))
for i in range (1,inputs+1):
    num= float(input("Please enter your numbers one by one: "))
    sum+=num
def avg(sum,inputs):
    return sum/inputs
print("Average of the numbers is ",(avg(sum,inputs)))



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





