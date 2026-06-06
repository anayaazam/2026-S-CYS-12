#Task 1: Function Call
def hello():
    print("hello world")
hello()


#Task 2:
def info():
    print("Name:Anaya\t Reg.2026-S-CYS-12\t Section:A")
info()


#Task 3:
def sum(a,b):
    return a+b
sum(2,5)
print(sum(a=1,b=2))


#Task 4:
def sum(a,b):
    return a+b
sum(1,2)
print(sum(1,2))
c=5
d=8
a= sum (c,d)
print (a)


#Task 5:
l = len("Anaya")
print(l)


#Task 6:
M =max(10,20)
print (M)
M = max(20,20)
print (M)


#Task 7:
m = min(-20,20)
print(m)


#Task 8:
print(type(5))
print(type(5.5))
print(type("b"))


#Task 9:
sen = input("Enter input here:")
def typ(sen):
    print(type(sen))
typ(hello)


#Task 10:
def greet (name,rollnum):
    print(f"Hello {name},your Registration number is 2026-S-CYS-{rollnum}")
greet("anaya",12)