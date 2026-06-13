# Task 5:
def show(n):
    if n==0:
        return
    print(n)
    print(n-1)
show(5)

# Task 6:
def fact(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n* fact(n-1)
print(fact(1))
print(fact(5))
print(fact(6))

