# Task 1 : Permutation and Combination
import math

n= int(input("Enter value of n: "))
r= int(input("Enter value of r: "))

print("The total number of combinations are",math.comb(n,r))
print("The total number of permutations are",math.perm(n,r))
