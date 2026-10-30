// Task_26: [non_oop]
// Armstrong numbers from 1 to 1000
public class Task_26 {
    static int intPower(int base, int exponent) {
        int result = 1;
        for (int i = 0; i < exponent; i++) result = result * base;
        return result;
    }
    public static void main(String[] args) {
        System.out.println("Armstrong numbers from 1 to 1000:");
        for (int number = 1; number <= 1000; number++) {
            int digitCount = 0;
            int temp = number;
            while (temp > 0) {
                digitCount++;
                temp = temp / 10;
            }
            int sum = 0;
            temp = number;
            while (temp > 0) {
                sum = sum + intPower(temp % 10, digitCount);
                temp = temp / 10;
            }
            if (sum == number) System.out.print(number + " ");
        }
        System.out.println();
    }
}
