#Task 1: Single,  Double, Triple Quotes
print('Hello World')
print("Hello World")
print('''Hello World''')
print("'Hello World'")
print('"Hello World"')



#Task 2: Print Function
a = 34
b= 65
sum = a + b
print(sum)



#Task 3: Print Function with Concatenation Operator
name= "Anaya"
age= "19"
print(" Hello my name is " + name + " and I'm " + age + " years old. ")


#Task 4: Escape Sequences
# \n
print("Hello\nWorld")
#\t
print("Hello\tWorld")



#Task 5: Format Specifiers
# %d
n=23.43
print("%d" %n)

# %e
n=12
print("%2e"%n)

# %f
n=32
print("%f"%n)

# %o
n=8
print("%o"%n)

# %x
n=16
print("%x"%n)


#Task 6: Days of Week
print("Monday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday")



#Task 7: Languages
print("Languages:\n\tPython\n\tJava\n\tJavaScript")



#Tasks 8: Pattern
n=6
for i in range(n):
    for j in range(i):
        print ("*",end=" ")
    print()
r=4
for i in range(r):
    for j in range(i,r):
        print ("*",end=" ")
    print ()



#Task 9: 200x
print("Pakistan Zindabad\t"*200)



#Task 10: Input
name = input("Enter your name:")
reg_no = int(input("Enter your registration number:"))
dep_name = input("Enter your department name:")
sem = int(input("Enter your semester:"))

print (f"Name:{name}\tReg.no:{reg_no}\tDepartment:{dep_name}\tSemester:{sem}")
