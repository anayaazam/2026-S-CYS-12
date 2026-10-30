// Task_13: [oop]
// BankAccount
public class Task_13 {
    static class BankAccount {
        private double balance;
        BankAccount(double openingBalance) { balance = openingBalance; }
        void deposit(double amount) {
            if (amount <= 0) {
                System.out.println("Deposit " + amount + " rejected (invalid amount)");
            } else {
                balance = balance + amount;
                System.out.println("Deposited " + amount);
            }
            System.out.println("   Balance: " + balance);
        }
        void withdraw(double amount) {
            if (amount <= 0) {
                System.out.println("Withdraw " + amount + " rejected (invalid amount)");
            } else if (amount > balance) {
                System.out.println("Withdraw " + amount + " rejected (not enough money)");
            } else {
                balance = balance - amount;
                System.out.println("Withdrew " + amount);
            }
            System.out.println("   Balance: " + balance);
        }
        double getBalance() { return balance; }
    }
    public static void main(String[] args) {
        BankAccount account = new BankAccount(500);
        System.out.println("Opening balance: " + account.getBalance());
        account.deposit(200);
        account.withdraw(300);
        account.withdraw(1000);
        account.deposit(-50);
        account.withdraw(400);
    }
}
