# Task 11:
# in an existing file named "data.txt" add some content
a = open("data.txt","a")
s = a.write("hello")
a.close()
print(s)

# Task 12:
import os
os.mkdir("anayaazam")
# Task 13:
for i in range(1,100):
    os.mkdir(f"day {i+1}")

