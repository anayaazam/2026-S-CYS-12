# Task 1: Miles to Kilometer
m = float(input("Miles:"))
km = m * 1.609
print("Kilometers:", km)



# Task 2: Swapping Two Numbers
x = int(input("Enter a value of x:"))
y = int(input("Enter a value of y:"))
print(f'x={x},y={y}')
temp = x
x = y
y = temp
print(x)
print(y)



# Task 3: Celsius to Fahrenheit
C = float(input("Celsius:"))
F = (9 / 5) * C + 32
print("Fahrenheit:", F)



# Task 4: Hours
hours = float(input("Hours:"))
weeks = hours / (24 * 7)
days = hours / 24
print("Weeks:", weeks)
print("Days:", days)
print("Hours:", hours)



# Task 5: Cube or not
num1 = int(input("Enter a number:"))
num2 = int(input("Enter another number:"))
cube1 = num1 ** 3
if num2 == cube1:
    print("The second number is the cube of the first")
else:
    print("The second number is not the cube of the first")



# Task 6:  Average
s1 = int(input("Enter marks of first subject:"))
s2 = int(input("Enter marks of second subject:"))
s3 = int(input("Enter marks of third subject:"))
total = s1 + s2 + s3
avg = total / 3
if avg > 75:
    print("You are above standard")
    print("Admission Granted")
else:
    print("You are below standard")



# Task 7: Bonus Salary
salary = float(input("Enter your salary:"))
scale = int(input("Enter your scale:"))
total = 0
if scale > 16:
    bonus = salary *0.40
    print("Your bonus(40%):", bonus)
    total = bonus + salary
elif scale <= 16:
    bonus = salary *0.20
    print("Your bonus(20%):", bonus)
    total = bonus + salary
print(float(total))




# Task 8: CGPA
num_subjects = int(input("Enter the number of subjects: "))
total_grd_pts = 0
total_crd_hrs = 0
for i in range(num_subjects):
    print(f"\nSubject {i + 1}:")
    subject_name = input("Subject name: ")
    gpa = float(input("Enter GPA for this subject: "))
    crd_hrs = int(input("Enter credit hours for this subject: "))

    total_grd_pts += gpa * crd_hrs
    total_crd_hrs += crd_hrs

if total_crd_hrs > 0:
    cgpa = total_grd_pts / total_crd_hrs
    print(f"Total Grade Points: {total_grd_pts:.2f}")
    print(f"Total Credit Hours: {total_crd_hrs}")
    print(f"Your CGPA is: {cgpa:.2f}")
else:
    print("Total credit hours cannot be zero!")



# Task 9: 24-hour Format
hrs = int(input("Enter hours:"))
mins = int(input("Enter minutes:"))
if hrs > 24 or mins > 59 or hrs < 0 or mins < 0:
    print("Out of range")
elif hrs == 24:
    hrs = 12
    time = "a.m."
else:
    time = " "
    if hrs > 12:
        hrs = hrs - 12
        time = "p.m."
    elif hrs == 0:
        hrs = 12
        time = "p.m."
    elif hrs == 24:
        hrs = 12
        time = "a.m."
    elif hrs == 12:
        hrs = hrs
        time = "p.m."
print(f"The time is {hrs}:{mins:02d} {time}")



# Task 10: Quadrants
x = int(input("Enter a x-value:"))
y = int(input("Enter a y-value:"))
if x > 0 and y > 0:
    print("First Quadrant")
elif x < 0 and y > 0:
    print("Second Quadrant")
elif x < 0 and y < 0:
    print("Third Quadrant")
elif x > 0 and y < 0:
    print("Fourth Quadrant")




# Task 11: Electricity Bill
units = int(input("Enter your units:"))
bill = 0
if units <= 100:
    bill = units*10
elif units <= 200:
    bill = units*20
elif units <= 300:
    bill = units*30
elif units > 300:
    bill = units*40
print(f"Your electricity bill is : {bill}")



