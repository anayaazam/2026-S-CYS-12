# pattrens
# Task 1
for i in range(4):
    for j in range(4):
        print(f"{i},{j}")


# Task 2
for i in range(4):
    for j in range(4):
        print("*",end=" ")
    print()


# Task 3
for i in range(1,6):
    for j in range(1,6):
        print("*",end=" ")
    print()


# Task 4
for i in range(1,5):
    for j in range(i):
        print("*",end=" ")
    print()


# Task 5
for i in range(1,5):
    for j in range(i):
        print(j,end=" ")
    print()


# Task 6
for i in range(1,5):
    for j in range(i+1):
        print(j,end=" ")
    print()


# Task 7
for i in range(1,5):
    for j in range(1,i+1):
        print(j,end=" ")
    print()


# Task 8
for i in range(1,5):
    for j in range(0,i+1):
        print(j,end=" ")
    print()


# Task 9
for i in range(1,5):
    for j in range(-1,i+1):
        print(j,end=" ")
    print()


# Task 10
for i in range(1,5):
    for j in range(1,5):
        print(j,end=" ")
    print()


# Task 11
for i in range(1,11):
    for j in range(1,5):
        print(i*j,end=" \t")
    print()


# Task 12
for i in range(1,5):
    for j in range(1,11):
        print(i*j,end=" \t")
    print()


# Task 13
for i in range(1,5):
    for j in range(4-i):
        print(" ",end="")
    for j in range(2*i-1):
        print("*",end="")
    print ()
for i in range (4,0,-1):
    for j in range(4-i):
        print (" ",end="")
    for j in range(2*i-1):
        print("*",end="")
    print ()