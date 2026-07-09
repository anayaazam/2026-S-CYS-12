# Task 01:
def square(num):
    print(num**2)
    return
square(5)


# Task 02:
a =lambda x: x**2
print(a(5))


# Task 03:
a = lambda x,y: x+y
print(a(3,6))


# Task 04:
a = lambda x,y,z: x+y+z
print(a(3,6,5))


# Task 05:
a= [1,2,3,4]
b = list(map(lambda x: x**2,a))
print(b)


# Task 06:
x ="25"
y = "anaya"
print(x)
print(y)
print(x+y)


# Task 07:
x =45
def a():
    x = 40
    print(x)
    print(globals()["x"])
a()
    
    
# Task 08:
# make a file named "anayaazam"
def welcome():
    print("Welcome to the class!")
    return
if __name__ == "__main__" :
    welcome()
def ushna():
    print("Shna")
    return
    
# in another file import the functions from the file "anayaazam"
import anayaazam
anayaazam.welcome()
anayaazam.ushna()


# Task 09:
# first make a file named "data.txt"
# to write in it use write
a = open("data.txt","w")
s = a.write("welcome")
a.close()
print(s)


# Task 10:
# read a file named "data.txt"
a = open("data.txt","r")
s = a.read()
a.close()
print(s)


# Task 11:
# in an existing file named "data.txt" add some content
a = open("data.txt","a")
s = a.write("hello")
a.close()
print(s)


# Task 12:
import os
os.mkdir("anayaazam")
# Task 13:
for i in range(1,100):
    os.mkdir(f"day {i+1}")
