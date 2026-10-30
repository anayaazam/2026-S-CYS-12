import java.util.Scanner;

// Task_06: [non_oop]
// print digits in reverse (1200 -> 0021), no String
public class Task_06 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter an integer: ");
        long n = sc.nextInt();
        if (n < 0) {
            System.out.print("-");
            n = -n;
        }
        if (n == 0) {
            System.out.print(0);
        }
        while (n > 0) {
            System.out.print(n % 10);
            n = n / 10;
        }
        System.out.println();
    }
}
