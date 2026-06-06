#Task 1:
s= {1,2,3,3}
print(s)


#Task 2:
s = {1,2,3,"anaya"}
print(s)


#Task 3:
E =set({})
print(type(E))


#Task 4:
a = set([1,2,3,4])
print(type(a))


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


#Task 7:
s = {"CE","CS","DS","SE","IST","IT","CE"}
print(s)
s.remove("CE")
print(s)


#Task 8:
s = {"CE","CS","DS","SE","IST","IT","CE"}
s.clear()
print(s)
print(type(s))


#Task 9:
s = {"CE","CS","DS","SE","IST","IT","CE"}
s.pop()
print(s)
s.pop()
print(s)


#Task 10:
s1 = {10,12,13,14,17}
s2 = {"anaya","fatima","ushna","fizza","eshaal"}
s3 = {1,"cat",(1,2,3)}
print(s.union(s1,s2,s3))
s1.update(s2)
print(s1)
print(s2)


#Task 11:
s1 = {"UET","NUST","ITU","LUMS"}
s2 = {"hello","world"}
print(s1.intersection(s2))


#Task 12:
s1 = {1,2,3,4,5,6,7,8,9,10}
s2 = {10,11,12,13,14,15,16,17,18,19}
s3 = {10,20,30,40,50,60,70,80,90,100}
s1.intersection_update(s2)
print(s1)


#Task 13:
s = s1.symmetric_difference(s2)
print(s)
print(s1)
print(s2)


#Task14:
s = s1.isdisjoint(s2)
print(s)


#Task 15:
s1 = {1,2,3,4}
s2 = {5,6,7,8}
s = s1.isdisjoint(s2)
print(s)


#Task 16:
s1 = {1,2,3,4,5,6,7,8,9,10}
s2 ={2,4,6,8,10}
print(s2.issubset(s1))