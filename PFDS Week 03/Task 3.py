#Task 3 : Capital and Reverse
string= str(input("Enter sentence:"))
def  l_u(answer):
    return answer.upper()
lambda answer: answer.upper()

reverse_string = lambda r: r[::-1]

if str.islower(string):
    text= l_u(string)
    print(text)
elif str.isupper(string):
    print("Reverse:",reverse_string(string))
else:
    print("Please enter a valid sentence")
