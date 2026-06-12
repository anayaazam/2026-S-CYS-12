# Task 11:
# in an existing file named "data.txt" add some content
a = open("data.txt","a")
s = a.write("hello")
a.close()
print(s)
