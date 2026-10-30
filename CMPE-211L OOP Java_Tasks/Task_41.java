// Task_41: [oop]
// checked exception + finally with return
public class Task_41 {
    static class InsufficientFundsException extends Exception {
        InsufficientFundsException(String message) { super(message); }
    }
    static class Account {
        private double balance;
        Account(double balance) { this.balance = balance; }
        void withdraw(double amount) throws InsufficientFundsException {
            if (amount > balance) {
                throw new InsufficientFundsException(
                        "Cannot withdraw " + amount + ", balance is only " + balance);
            }
            balance = balance - amount;
        }
        double getBalance() { return balance; }
    }
    static String finallyDemo() {
        try {
            System.out.println("  inside try: about to return");
            return "value returned from try";
        } finally {
            System.out.println("  inside finally: still runs!");
        }
    }
    public static void main(String[] args) {
        Account account = new Account(100);
        try {
            account.withdraw(30);
            System.out.println("Withdrew 30, balance = " + account.getBalance());
            account.withdraw(500);
            System.out.println("This line is never reached");
        } catch (InsufficientFundsException e) {
            System.out.println("Caught: " + e.getMessage());
        }
        System.out.println("finally demo:");
        System.out.println("  result = " + finallyDemo());
    }
}
