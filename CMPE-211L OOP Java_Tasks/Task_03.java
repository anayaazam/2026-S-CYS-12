import java.util.Scanner;

// Task_03: [non_oop]
// median of three numbers (no arrays, no sorting)
public class Task_03 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter first number: ");
        double a = sc.nextDouble();
        System.out.print("Enter second number: ");
        double b = sc.nextDouble();
        System.out.print("Enter third number: ");
        double c = sc.nextDouble();

        double median;
        if ((a >= b && a <= c) || (a <= b && a >= c)) {
            median = a;
        } else if ((b >= a && b <= c) || (b <= a && b >= c)) {
            median = b;
        } else {
            median = c;
        }
        System.out.println("Median = " + median);
    }
}
