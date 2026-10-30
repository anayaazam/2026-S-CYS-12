// Task_37: [oop]
// immutable Money class, == versus equals()
public class Task_37 {
    static final class Money {
        private final int amount;
        private final String currency;
        Money(int amount, String currency) {
            this.amount = amount;
            this.currency = currency;
        }
        Money add(Money other) {

            return new Money(this.amount + other.amount, currency);
        }
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Money)) return false;
            Money other = (Money) o;
            return amount == other.amount && currency.equals(other.currency);
        }
        public int hashCode() {
            return 31 * amount + currency.hashCode();
        }
        public String toString() { return amount + " " + currency; }
    }
    public static void main(String[] args) {
        Money m1 = new Money(100, "USD");
        Money m2 = new Money(100, "USD");
        Money m3 = m1;
        System.out.println("m1 == m2      : " + (m1 == m2));
        System.out.println("m1.equals(m2) : " + m1.equals(m2));
        System.out.println("m1 == m3      : " + (m1 == m3));
        System.out.println("same hashCode : " + (m1.hashCode() == m2.hashCode()));
        Money sum = m1.add(m2);
        System.out.println("m1 + m2 = " + sum + "   (m1 is still " + m1 + ")");
    }
}
