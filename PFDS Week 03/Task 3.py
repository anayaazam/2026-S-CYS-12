#Task 4 : Fahrenheit and Celsius Conversions
temp = float(input("Enter temperature here="))
unit = input("Enter units here( 'C' for Celsius and 'F' for Fahrenheit)=")

def celsius_to_fahrenheit(c):
    return ((c*9/5)+32)

def fahrenheit_to_celsius(f):
    return ((f-32)*5/9)

if unit.upper()=="C":
    result = fahrenheit_to_celsius(temp)
    print("Temperature in Celsius is ",result)
elif unit.upper() =="F":
    result = celsius_to_fahrenheit(temp)
    print("Temperature in Fahrenheit is ", result)
else:
    print("Invalid unit. Enter F or C")
