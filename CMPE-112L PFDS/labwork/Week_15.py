# Task 1: Function
def greet():
    name = input("Enter your name here:")
    print(f'Hello! {name}')
greet()


# Task 2:
def info():
    name = input("Enter your name here:")
    roll_no = input("Enter your roll no:")
    dep = input("Enter your department here:")
    print(f"Name:{name}\t Roll.no:{roll_no}\t Department:{dep}")
info()


# Task 3:
def show(n):
    print(n)
show(5)

# Task 4:
def show(n):
    print(n)
    print(n-1)
show(5)


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


# Task 7:
# def fact(n):
#     return n*fact(n-1)
# print(fact(5))    # will show error as maximum recursion depth is reached


# Task 8: Fibonacci Sequence with recursion
def fibonacci(n):
    if n<=0:
        return []
    elif n == 1:
        return [0]
    elif n==2:
        return [0, 1]
    else:
        seq = fibonacci(n-1)
        seq.append(seq[-1]+seq[-2])
        return seq
print(fibonacci(5))


# Task 9:
def hello():
    try:
        a = input("Enter your name here:")
        print(f'Hello {a}!')
        print("Hello World!")
    except:
        print("Invalid input")
print(hello())


# Task 10:
def hello():
    try:
        a = input("Enter your name here:")
        print(f'Hello {a}!')
        print("Hello World!")
    except Exception as e:
        print("Error")
print(hello())
