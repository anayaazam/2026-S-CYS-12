import java.util.Scanner;

// Task_11: [non_oop]
// first N Fibonacci numbers with three variables
public class Task_11 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter N: ");
        int n = sc.nextInt();
        long first = 0, second = 1, next;
        for (int i = 0; i < n; i++) {
            System.out.print(first + " ");
            next = first + second;
            first = second;
            second = next;
        }
        System.out.println();
    }
}
