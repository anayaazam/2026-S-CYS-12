# Task 1: Binary  to Decimal Equivalent
bin = (input("Enter your binary number: "))
decimal=0
power=0
i=len(bin)-1
while i>=0:
    decimal+=int(bin[i])*(2**power)
    power+=1
    i-=1
print(f"decimal equivalent is:",decimal)
