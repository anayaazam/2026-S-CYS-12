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

