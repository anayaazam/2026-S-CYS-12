#Task 2: Vowels and consonants
sentence= input("Enter your sentence:")
vowels =0
consonants =0
i=0
for i in range (len(sentence)):
    if sentence[i] in 'aeiou'or sentence[i] in 'AEIOU':
        vowels +=1
    else:
        consonants +=1
print("vowels:",vowels)
print("consonants:",consonants)
