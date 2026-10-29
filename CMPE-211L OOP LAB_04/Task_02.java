import java.util.Scanner;
public class Task_02 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Customer name: ");
        String name = sc.nextLine();
        double opening;
        while (true) {
            System.out.print("Opening balance: ");
            opening = readAmount(sc);
            if (opening >= 0) break;
            System.out.println("Please enter a valid number (0 or more).");
        }
        SavingAccount account = new SavingAccount(name, opening);
        boolean running = true;
        while (running) {
            System.out.println();
            System.out.println("===== SAVING ACCOUNT MENU =====");
            System.out.println("1. Deposit money");
            System.out.println("2. Withdraw money");
            System.out.println("3. Check balance");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");
            if (!sc.hasNextLine()) break;
            int choice;
            try {
                choice = Integer.parseInt(sc.nextLine().trim());
            } catch (NumberFormatException e) {
                System.out.println("Please type a number from 1 to 4.");
                continue;
            }
            switch (choice) {
                case 1:
                    System.out.print("Amount to deposit: ");
                    account.deposit(readAmount(sc));
                    break;
                case 2:
                    System.out.print("Amount to withdraw: ");
                    account.withdraw(readAmount(sc));
                    break;
                case 3:
                    account.checkBalance();
                    break;
                case 4:
                    System.out.println("Thank you, " + account.getName() + ". Goodbye!");
                    running = false;
                    break;
                default:
                    System.out.println("Invalid choice. Please pick 1, 2, 3 or 4.");
            }
        }
    }
    static double readAmount(Scanner sc) {
        if (!sc.hasNextLine()) return -1;
        try {
            double v = Double.parseDouble(sc.nextLine().trim());
            if (Double.isNaN(v) || Double.isInfinite(v)) return -1;
            return v;
        } catch (NumberFormatException e) {
            return -1;
        }
    }
}
class SavingAccount {
    private String name;
    private double balance;
    public SavingAccount(String name, double initialBalance) {
        this.name = name;
        if (initialBalance >= 0) {
            balance = initialBalance;
        } else {
            System.out.println("Opening balance cannot be negative. Starting with 0.");
            balance = 0;
        }
    }
    public String getName() { return name; }
    public void deposit(double amount) {
        if (amount <= 0) {
            System.out.println("Invalid amount. Deposit must be more than 0.");
            return;
        }
        balance = balance + amount;
        System.out.println("Deposited " + amount + ". New balance: " + balance);
    }
    public void withdraw(double amount) {
        if (amount <= 0) {
            System.out.println("Invalid amount. Withdrawal must be more than 0.");
        } else if (amount > balance) {
            System.out.println("Not enough money. Your balance is only " + balance);
        } else {
            balance = balance - amount;
            System.out.println("Withdrew " + amount + ". New balance: " + balance);
        }
    }
    public void checkBalance() {
        System.out.println(name + ", your current balance is: " + balance);
    }
}
