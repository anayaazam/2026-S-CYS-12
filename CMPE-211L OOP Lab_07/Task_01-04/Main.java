// Task_09
public class Main {
    public static void main(String[] args) {
        Bank hbl = new Bank("HBL");
        Bank ubl = new Bank("UBL");

        Client ali = hbl.addClient(new Person("Ali Khan", "35202-1111111-1", "0300-1111111"));
        Client sara = hbl.addClient(new Person("Sara Ahmed", "35202-2222222-2", "0300-2222222"));

        System.out.println("--- Adding accounts ---");
        hbl.addAccount("H-101", 5000, ali);
        hbl.addAccount("H-102", 12000, ali);
        hbl.addAccount("H-201", 8000, sara);
        hbl.addAccount("H-101", 100, sara);

        ubl.addClient(ali);
        ubl.addAccount("U-301", 3000, ali);

        System.out.println("\n--- Client details ---");
        System.out.println(ali);
        System.out.println(sara);

        System.out.println("--- Deposit / Withdraw ---");
        System.out.println("Deposit 1000 to H-101: " + ali.deposit(1000, "H-101"));
        System.out.println("Withdraw 2500 from H-102: " + ali.withdraw(2500, "H-102"));
        System.out.println("Withdraw 99999 from H-101: " + ali.withdraw(99999, "H-101"));
        System.out.println("Deposit to unknown account: " + ali.deposit(50, "X-000"));

        System.out.println("\n--- Totals ---");
        System.out.println("Ali total (all banks): " + ali.totalAmount());
        System.out.println("HBL total: " + hbl.totalAmount());
        System.out.println("UBL total: " + ubl.totalAmount());

        System.out.println("\n--- Searching ---");
        System.out.println(hbl.searchAccount("H-201"));
        System.out.println("Search missing account: " + hbl.searchAccount("Z-999"));
        System.out.println(hbl.searchCustomerDetail("35202-2222222-2"));
        System.out.println("Search missing CNIC: " + hbl.searchCustomerDetail("00000-0000000-0"));

        System.out.println("\n--- Removing Ali from HBL ---");
        System.out.println("Removed: " + hbl.removeClient(ali.getId()));
        System.out.println(hbl);
        System.out.println(ali);
        System.out.println("Removing again: " + hbl.removeClient(ali.getId()));

        System.out.println("\n--- Bank summaries ---");
        System.out.println(hbl);
        System.out.println(ubl);
    }
}
