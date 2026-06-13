# Assignment 1(theater seating)
seats = [
    [10,10,10,10,10,10,10,10,10,10],
    [10,10,10,10,10,10,10,10,10,10],
    [10,10,10,10,10,10,10,10,10,10],
    [10,10,20,20,20,20,20,20,10,10],
    [10,10,20,20,20,20,20,20,10,10],
    [10,10,20,20,20,20,20,20,10,10],
    [20,20,30,30,40,40,30,30,20,20],
    [20,30,30,40,50,50,40,30,30,20],
    [30,40,50,50,50,50,50,40,30,30],
    [30,40,50,50,50,50,50,40,30,30]]
def display_chart():
    print("\nSeat Numbers")
    print("1  2  3  4  5  6  7  8  9 10")
    for i in range(len(seats)):
        print(f"Row {i+1:2}", end="  ")
        for price in seats[i]:
            print(f"{price:2}", end=" ")
        print()
while True:
    display_chart()
    choice = input(
        "\nChoose an option:\n"
        "1. Select a seat\n"
        "2. Select by price\n"
        "3. Exit\n"
        "Enter choice: "
    )
    if choice == "1":
        row = int(input("Enter row (1-10): ")) - 1
        col = int(input("Enter seat number (1-10): ")) - 1
        if 0 <= row < 10 and 0 <= col < 10:
            if seats[row][col] != 0:
                print(f"Seat booked. Price = ${seats[row][col]}")
                seats[row][col] = 0
            else:
                print("Seat already sold.")
        else:
            print("Invalid seat.")
    elif choice == "2":
        price = int(input("Enter desired price: "))
        found = False
        for r in range(10):
            for c in range(10):
                if seats[r][c] == price:
                    print(f"Seat found at Row {r+1}, Seat {c+1}")
                    seats[r][c] = 0
                    found = True
                    break
            if found:
                break
        if not found:
            print("No available seat at that price.")
    elif choice == "3":
        print("Thank you!")
        break
    else:
        print("Invalid choice.")
        
# Assingment 2 (best_customer)
def Best_Customer(sales, customers):
    max_sales = sales[0]
    best_customer = customers[0]
    for i in range(1, len(sales)):
        if sales[i] > max_sales:
            max_sales = sales[i]
            best_customer = customers[i]
    return best_customer
sales = []
customers = []
while True:
    amount = float(input("Enter purchase amount (Enter 0 to stop): "))
    if amount == 0:
        break
    name = input("Enter customer name: ")
    sales.append(amount)
    customers.append(name)
if len(sales) > 0:
    best = Best_Customer(sales, customers)
    print("\nBest Customer of the Day:", best)
else:
    print("No customer data entered.")
