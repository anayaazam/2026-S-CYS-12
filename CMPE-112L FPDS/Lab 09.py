# Task 1: Grades(for)
students = int(input("Enter number of students: "))
for i in range(students):
    name = input("Enter name: ")
    roll_no = int(input("Enter roll number: "))
    obt_marks = int(input("Enter your marks: "))
    total_marks = int(input("Enter your total marks: "))
    print(name)
    print(roll_no)
    print(obt_marks)
    print(total_marks)
    if obt_marks < total_marks:
        percentage = (obt_marks / total_marks)* 100
        print (percentage)
        if percentage >= 90:
            print("A")
        elif percentage >= 85:
            print("A-")
        elif percentage >= 80:
            print("B+")
        elif percentage >= 75:
            print("B")
        elif percentage >= 70:
            print("B-")
        elif percentage >= 65:
            print("C+")
        elif percentage >= 60:
            print("C")
        elif percentage >= 55:
            print("C-")
        elif percentage >= 50:
            print("D")
        elif percentage < 50:
            print("F")
    elif obt_marks > total_marks:
        print ("Not Valid")
    elif total_marks == 0:
        print ("Not Defined")
    elif obt_marks == total_marks:
        print ("100%")


# Task 2: Grades(while)
students = int(input("Enter number of students: "))
i=1
while i<=students:
    name = input("Enter name: ")
    roll_no = int(input("Enter roll number: "))
    obt_marks = int(input("Enter your marks: "))
    total_marks = int(input("Enter your total marks: "))
    print("Name :",name)
    print("RollNo :",roll_no)
    print("Obtained :",obt_marks)
    print("Total :",total_marks)
    if obt_marks < total_marks:
        percentage = (obt_marks / total_marks)* 100
        print (percentage)
        if percentage >= 90:
            print("A")
        elif percentage >= 85:
            print("A-")
        elif percentage >= 80:
            print("B+")
        elif percentage >= 75:
            print("B")
        elif percentage >= 70:
            print("B-")
        elif percentage >= 65:
            print("C+")
        elif percentage >= 60:
            print("C")
        elif percentage >= 55:
            print("C-")
        elif percentage >= 50:
            print("D")
        elif percentage < 50:
            print("F")
    elif obt_marks > total_marks:
        print ("Not Valid")
    elif total_marks == 0:
        print ("Not Defined")
    elif obt_marks == total_marks:
        print ("100%")
    i=i+1


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