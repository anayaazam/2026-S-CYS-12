// Task_03
import java.util.ArrayList;
import java.util.List;

class Client {
    private static int count = 0;

    private String id;
    private Person personDetails;
    private List<Account> accounts = new ArrayList<>();

    public Client(Person personDetails) {
        count++;
        this.id = "C" + count;
        this.personDetails = personDetails;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public Person getPersonDetails() { return personDetails; }
    public void setPersonDetails(Person personDetails) { this.personDetails = personDetails; }

    public List<Account> getAcList() { return accounts; }
    public void setAcList(List<Account> acList) {
        this.accounts = (acList != null) ? acList : new ArrayList<>();
    }

    public static int getCount() { return count; }

    public float totalAmount() {
        float total = 0;
        for (Account a : accounts) {
            total += a.getAmount();
        }
        return total;
    }

    public void addAccount(Account a) {
        if (a != null && !accounts.contains(a)) {
            accounts.add(a);
        }
    }

    private Account findAccount(String accNo) {
        for (Account a : accounts) {
            if (accNo != null && accNo.equals(a.getNumber())) return a;
        }
        return null;
    }

    // Returns the new balance, or -1 if the account is not found / withdrawal fails
    public float withdraw(float amount, String accNo) {
        Account a = findAccount(accNo);
        if (a == null) {
            System.out.println("Account " + accNo + " not found for client " + id + ".");
            return -1;
        }
        return a.withdraw(amount);
    }

    // Returns the new balance, or -1 if the account is not found / deposit fails
    public float deposit(float amount, String accNo) {
        Account a = findAccount(accNo);
        if (a == null) {
            System.out.println("Account " + accNo + " not found for client " + id + ".");
            return -1;
        }
        return a.deposit(amount);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Client ID: ").append(id).append("\n");
        sb.append(personDetails).append("\n");
        if (accounts.isEmpty()) {
            sb.append("  No accounts.\n");
        } else {
            for (Account a : accounts) {
                sb.append("  Account ID: ").append(a.getNumber())
                  .append(", Amount: ").append(a.getAmount()).append("\n");
            }
        }
        return sb.toString();
    }
}
