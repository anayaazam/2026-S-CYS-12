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

