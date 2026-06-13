#Task 8: Total(*numbers)
#variable length arguments
def sum_all(*args):
    return sum(args)
print (sum_all(1,2,3,4,5,6,7,8,9))
print (sum_all(193,345))
print(sum_all(112,366,864,345,234,456,567))
print (sum_all(26,36,67,38,95,85,54,65,63,32,52))

#Task 9: Average(*numbers)
sum=0
inputs= int(input("Please enter your number of inputs: "))
for i in range (1,inputs+1):
    num= float(input("Please enter your numbers one by one: "))
    sum+=num
def avg(sum,inputs):
    return sum/inputs
print("Average of the numbers is ",(avg(sum,inputs)))

