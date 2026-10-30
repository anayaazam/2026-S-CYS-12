// Task_50: [non_oop]
// factorial of 50 without BigInteger
public class Task_50 {
    public static void main(String[] args) {
        int[] digits = new int[100];
        digits[0] = 1;
        int length = 1;
        for (int factor = 2; factor <= 50; factor++) {
            int carry = 0;
            for (int i = 0; i < length; i++) {
                int product = digits[i] * factor + carry;
                digits[i] = product % 10;
                carry = product / 10;
            }
            while (carry > 0) {
                digits[length] = carry % 10;
                length++;
                carry = carry / 10;
            }
        }
        System.out.print("50! = ");
        for (int i = length - 1; i >= 0; i--) System.out.print(digits[i]);
        System.out.println("  (" + length + " digits)");
    }
}
