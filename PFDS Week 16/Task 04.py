# Task 09:
# first make a file named "data.txt"
# to write in it use write
a = open("data.txt","w")
s = a.write("welcome")
a.close()
print(s)

# Task 10:
# read a file named "data.txt"
a = open("data.txt","r")
s = a.read()
a.close()
print(s)
