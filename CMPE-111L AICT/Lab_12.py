#Task 1: Count 1 and 3
def count_13(n):
    count_1 = 0
    count_3 = 0
    for digit in str(n):
        if int(digit)==1:
            count_1+=1
        elif int(digit)==3:
            count_3+=1
    print(f"Count_1 is {count_1} and  Count_3 is {count_3}")
count_13(523135343136)




#Task 2: Dictionary
z = {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','ten':'10'}
def check(num):
    if num in z:
        return True
    else :
        return False
check('one')
check('twenty')




#Task 3: Square Dictionary
n = {1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8, 8:9, 9:10, 10:11, 11:12, 12:13, 13:14, 14:15}
for key in n:
    n[key] = n[key]**2
print(n)



#Task 4: Countdown Function
def count_down(x):
    while x>0:
        x-=1
        print(x)
    if x==0:
        print("Countdown is stopped!")
count_down(5)



#Task 5: Max Function
def maximum(x,y):
    m = max(x,y)
    return m
def cube(m):
    return m*m*m
print(cube(maximum(3,4)))




