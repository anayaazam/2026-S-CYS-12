import java.util.Scanner;

// Task_01: [non_oop]
// even or odd without using the % operator
public class Task_01 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter an integer: ");
        int n = sc.nextInt();
        if (n / 2 * 2 == n) {
            System.out.println(n + " is even");
        } else {
            System.out.println(n + " is odd");
        }
    }
}
