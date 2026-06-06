#Task 1: Sum list
l1 = [10,20,30,40,50]
l2 = [60,70,80,90,100]
sum_list = []
for i in range (len(l1)):
    sum = l1[i] + l2[i]
    sum_list.append(sum)
print(sum_list)



#Task 2: Multiplied List
l1 = [1,2,3,4,5,6,7,8,9,10]
mul_list = []
for e in l1:
    mul_list.append(e**2)
print(mul_list)



#Task 3: Even and Odd List
l1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
even_list = []
odd_list = []
for e in l1:
    if e % 2 == 0:
        even_list.append(e)
    else:
        odd_list.append(e)
print(f"even_list: {even_list}")
print(f"odd_list: {odd_list}")




#Task 4: 3x3 Matrix Manipulation
matrix = [ ]
for i in range(1,3):
    print(f'For Matrix {i}:')
    m = [ ]
    for j in range(1,4):
        r = [ ]
        for k in range(1,4):
            e = int(input(f"Enter element [{j}][{k}]:"))
            r.append(e)
        m.append(r)
    matrix.append(m)
M1 = matrix[0]
M2 = matrix[1]
print(f'M1 = {M1} \nM2 = {M2}')
result = [ ]
for i in range(3):
    row = [ ]
    for j in range(3):
        row.append(M1[i][j]+M2[i][j])
    result.append(row)
print(f'result = {result}')



#Task 5: Input Range and Prime Number List
n1 = int(input("Enter a start number:"))
n2 = int(input("Enter a end number:"))
l1 = []
prime_list = []
for i in range(n1,n2+1):
    l1.append(i)
    for j in range(2,i):
        if i%j==0:
            break
    else:
        prime_list.append(i)
print(f"list: {l1}")
print(f"prime_list: {prime_list}")


