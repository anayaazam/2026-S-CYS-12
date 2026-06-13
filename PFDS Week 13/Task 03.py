#Task 5:
s ={"CE","CS","DS","SE","CE","IST","IT"}
for x in s:
    print(x)
if "CE" in s:
    print("yes")

#Task 6:
s = {"CE","CS","DS","SE","IST","IT","CE"}
s.add("BE")
print(s)
s.discard("CE")
print(s)

