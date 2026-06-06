#Task 1 : Permutation and Combination
import math

n= int(input("Enter value of n: "))
r= int(input("Enter value of r: "))

print("The total number of combinations are",math.comb(n,r))
print("The total number of permutations are",math.perm(n,r))



#Task 2 : Larger Number and its Multiplication Table
num1 = int(input("Enter value of 1st number: "))
num2 = int(input("Enter value of 2nd number: "))

def compare(num1, num2):
    return max(num1, num2)
lambda max: max(num1, num2)
    max = max(num1, num2)
    print("The greater number is", max)

for i in range(1, 15):
    product = max * i
    print(product)
    i+=1


#Task 3 : Capital and Reverse
string= str(input("Enter sentence:"))
def  l_u(answer):
    return answer.upper()
lambda answer: answer.upper()

reverse_string = lambda r: r[::-1]

if str.islower(string):
    text= l_u(string)
    print(text)
elif str.isupper(string):
    print("Reverse:",reverse_string(string))
else:
    print("Please enter a valid sentence")



#Task 4 : Fahrenheit and Celsius Conversions
temp = float(input("Enter temperature here="))
unit = input("Enter units here( 'C' for Celsius and 'F' for Fahrenheit)=")

def celsius_to_fahrenheit(c):
    return ((c*9/5)+32)

def fahrenheit_to_celsius(f):
    return ((f-32)*5/9)

if unit.upper()=="C":
    result = fahrenheit_to_celsius(temp)
    print("Temperature in Celsius is ",result)
elif unit.upper() =="F":
    result = celsius_to_fahrenheit(temp)
    print("Temperature in Fahrenheit is ", result)
else:
    print("Invalid unit. Enter F or C")



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