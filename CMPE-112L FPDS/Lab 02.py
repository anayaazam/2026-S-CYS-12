#Task 1: Binary  to Decimal Equivalent
bin = (input("Enter your binary number: "))
decimal=0
power=0
i=len(bin)-1
while i>=0:
    decimal+=int(bin[i])*(2**power)
    power+=1
    i-=1
print(f"decimal equivalent is:",decimal)




#Task 2: Vowels and consonants
sentence= input("Enter your sentence:")
vowels =0
consonants =0
i=0
for i in range (len(sentence)):
    if sentence[i] in 'aeiou'or sentence[i] in 'AEIOU':
        vowels +=1
    else:
        consonants +=1
print("vowels:",vowels)
print("consonants:",consonants)




#Task 3:Display prime numbers in the range and their sum
start= int(input("Enter start a number:"))
end= int(input("Enter end a number:"))
sum=0
for i in range(start,end+1):
    for j in range(2,i):
        if i%j==0:
            break
    else:
        print(i)
        sum +=i
print("sum:",sum)




#Task 4: Password Generator
import string
import random
length = int(input("Enter the length of the password:"))

lower=string.ascii_lowercase
upper= string.ascii_uppercase
numbers = string.digits
symbols = string.punctuation
all= lower+upper+numbers+symbols
temp = random.sample(all,length)
password = "".join(temp)
print(password)




#Task 5: Draw a pattern
n=4
for i in range(n):
    for j in range(i+1):
        print("*",end=" ")
    print()
r=3
for i in range(r):
    for j in range(i,r):
        print("*",end=" ")
    print()











