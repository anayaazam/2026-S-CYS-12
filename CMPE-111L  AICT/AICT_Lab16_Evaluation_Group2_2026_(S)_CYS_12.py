#Task 1: Input Range and Prime Number List
n1 = int(input("Enter a start number:"))
n2 = int(input("Enter a end number:"))
list = []
prime_list = []
for i in range(n1,n2+1):
    list.append(i)
    for j in range(2,i):
        if i%j==0:
            break
    else:
        prime_list.append(i)
print(f"list: {list}")
print(f"prime_list: {prime_list}")

# Task 2: count_down()
def count_down():
    a =  int(input("Enter the number to start countdown:"))
    while a > 0:
        print(a)
        a-=1
    if a == 0:
        print("Countdown is stopped")
count_down()
