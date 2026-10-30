import java.util.Scanner;

// Task_02: [non_oop]
// swap two ints without a third variable
public class Task_02 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter a: ");
        int a = sc.nextInt();
        System.out.print("Enter b: ");
        int b = sc.nextInt();
        System.out.println("Before: a = " + a + ", b = " + b);
        a = a + b;
        b = a - b;
        a = a - b;
        System.out.println("After:  a = " + a + ", b = " + b);
    }
}
