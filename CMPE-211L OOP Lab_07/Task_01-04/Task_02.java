// Task_02
class Account {
    private static int count = 0;

    private String number;
    private float amount;
    private Client holder;

    // Default account: auto-generated number, zero balance, no holder
    public Account() {
        this(0f, null);
    }

    // Account with an auto-generated number
    public Account(float amount, Client holder) {
        count++;
        this.number = "A" + count;
        this.amount = Math.max(amount, 0f);
        this.holder = holder;
    }

    public Account(String number, float amount, Client holder) {
        count++;
        this.number = number;
        this.amount = Math.max(amount, 0f);
        this.holder = holder;
    }

    public String getNumber() { return number; }
    public void setNumber(String number) { this.number = number; }

    public float getAmount() { return amount; }
    public void setAmount(float amount) { this.amount = amount; }

    public Client getACholder() { return holder; }
    public void setACholder(Client holder) { this.holder = holder; }

    public static int getCount() { return count; }

    // Returns the new balance, or -1 if the withdrawal failed
    public float withdraw(float amt) {
        if (amt <= 0) {
            System.out.println("Invalid withdrawal amount.");
            return -1;
        }
        if (amt > amount) {
            System.out.println("Insufficient balance in account " + number + ".");
            return -1;
        }
        amount -= amt;
        return amount;
    }

    // Returns the new balance, or -1 if the deposit failed
    public float deposit(float amt) {
        if (amt <= 0) {
            System.out.println("Invalid deposit amount.");
            return -1;
        }
        amount += amt;
        return amount;
    }

    @Override
    public String toString() {
        String holderName = (holder != null && holder.getPersonDetails() != null)
                ? holder.getPersonDetails().getName() : "N/A";
        return "Account No: " + number + ", Balance: " + amount + ", Holder: " + holderName;
    }
}
