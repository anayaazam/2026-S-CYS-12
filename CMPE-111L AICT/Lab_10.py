#Task 1: Decimal to Binary Equivalent
n = int(input("Enter your number:"))
if n == 0:
    print("0")
else:
    bin_str = ""
    num = abs(n)
    while num > 0:
        remdr = num % 2
        bin_str = str(remdr) + bin_str
        num = num // 2
    if n < 0:
        bin_str = "-" + bin_str
    print(bin_str)



# Task 2: Range and Sum
n1 = int(input("Enter your start:"))
n2 = int(input("Enter your end:"))
sum = 0
for i in range(n1,n2+1):
    if i%2 == 0:
        sum = sum + i
    else:
        pass
print(f"Sum: {sum}")



#Task 3: Table from Range and number
num = int(input("Enter your number:"))
rng = int(input("Enter your range:"))
for i in range(1,rng+1):
    result = num * i
    print(f'{num} x {i} = {result}')



#Task 4: Divide by 2
n = int(input("Enter your number:"))
if n<0:
    print("Illegal input")
else:
    div = 0
    while n>=1:
        n= n/2
        div+=1
    print(f"The number of divisions are: {div}")
    print(f"The current number is {n}")


#Task 5: Number Guessing Game
level= input("Enter B for Basic, I fro Intermediate or E for Expert:")
tries = 0
if level == "B" or level == "b":
    tries=15
elif level == "I" or level == "i":
    tries=10
elif level == "E" or level == "e":
    tries=5
print(f"You have {tries} tries to guess the number")
ques = input("Do you want to decide a range? y/n")
guess = 0
if ques=="n":
    import random
    guess= random.randint(1,100)
elif ques=="y":
    a = int(input("Enter first number for range:"))
    b = int(input("Enter second number for range:"))
    import random
    guess = random.randint(a, b)
while tries>0:
    num = int(input("Enter number to guess:"))
    if num!=guess:
        if num>guess:
            print("Too high")
        elif num<guess:
            print("Too low")
    elif num==guess:
        print("Correct")
        break
    elif tries == 0:
        print("Out of guesses")
    tries-=1
    print(f"You have {tries} guesses left ")



#Task 6 : Number Pattern
for i in range(1,6):
    for j in range(0,i+1):
        print(j,end=" ")
    print()



#Task 7: Inverted Triangle
n=6
for i in range (n,1,-1):
    for j in range (i-1):
        print("#",end="")
    print()
