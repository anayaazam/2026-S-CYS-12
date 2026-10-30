import java.util.Scanner;

// Task_21: [non_oop]
// recursive fast exponentiation, count multiplications
public class Task_21 {
    static Scanner sc = new Scanner(System.in);

    static int multiplications = 0;

    static double power(double x, int n) {
        if (n == 0) return 1;
        double half = power(x, n / 2);
        if (n % 2 == 0) {
            multiplications = multiplications + 1;
            return half * half;
        } else {
            multiplications = multiplications + 2;
            return half * half * x;
        }
    }
    public static void main(String[] args) {
        System.out.print("Enter x: ");
        double x = sc.nextDouble();
        System.out.print("Enter n (0 or more): ");
        int n = sc.nextInt();
        if (n < 0) {
            System.out.println("Please use n >= 0");
            return;
        }
        multiplications = 0;
        System.out.println(x + "^" + n + " = " + power(x, n));
        multiplications = 0;
        double r = power(x, 30);
        System.out.println(x + "^30 = " + r);
        System.out.println("Multiplications used for n = 30: " + multiplications);
    }
}
