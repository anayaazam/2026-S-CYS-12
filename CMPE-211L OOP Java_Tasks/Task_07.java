import java.util.Scanner;

// Task_07: [non_oop]
// add digits until one digit is left
public class Task_07 {
    static Scanner sc = new Scanner(System.in);

    static int sumOfDigits(int n) {
        int sum = 0;
        while (n > 0) {
            sum = sum + n % 10;
            n = n / 10;
        }
        return sum;
    }

    public static void main(String[] args) {
        System.out.print("Enter a number: ");
        int n = sc.nextInt();
        if (n < 0) n = -n;
        System.out.print(n);
        while (n >= 10) {
            n = sumOfDigits(n);
            System.out.print(" -> " + n);
        }
        System.out.println();
    }
}
