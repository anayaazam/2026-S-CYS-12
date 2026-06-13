# Task 07:
x =45
def a():
    x = 40
    print(x)
    print(globals()["x"])
# Task 08:
# make a file named "anayaazam"
def welcome():
    print("Welcome to the class!")
    return
if __name__ == "__main__" :
    welcome()
def ushna():
    print("Shna")
    return
# in another file import the functions from the file "anayaazam"
import anayaazam
anayaazam.welcome()
anayaazam.ushna()

