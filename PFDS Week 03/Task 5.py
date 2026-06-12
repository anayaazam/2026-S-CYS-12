#Task 5 : Average GPA
subjects=int(input("Enter number of subjects: "))
print("Total Subject are",subjects)
total_credit_hours =0
total_grade_points =0
for i in range(1,subjects+1):
    gp = int(input("Enter Grade Points: "))
    credit = int(input("Enter credit hours: "))

    total_credit_hours += credit
    total_grade_points += credit*gp
print("Your credit hours are",total_credit_hours)
print("Your grade points are",total_grade_points)
if total_grade_points >0:
    GPA=(total_grade_points/total_credit_hours)
print("Your GPA for this semester is ",GPA)
else:
    print("You have not earned any credits for this semester")
