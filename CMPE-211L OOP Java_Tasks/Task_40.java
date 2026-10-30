import java.util.Scanner;

// Task_40: [non_oop]
// Tower of Hanoi
public class Task_40 {
    static Scanner sc = new Scanner(System.in);

    static int moves = 0;
    static void hanoi(int n, char from, char to, char helper) {
        if (n == 0) return;
        hanoi(n - 1, from, helper, to);
        moves++;
        System.out.println("Move disk " + n + " from " + from + " to " + to);
        hanoi(n - 1, helper, to, from);
    }
    public static void main(String[] args) {
        System.out.print("Number of disks (small, e.g. 3): ");
        int n = sc.nextInt();
        moves = 0;
        hanoi(n, 'A', 'C', 'B');
        int expected = 1;
        for (int i = 0; i < n; i++) expected = expected * 2;
        expected = expected - 1;
        System.out.println("Total moves = " + moves + ", 2^n - 1 = " + expected);
        if (moves == expected) System.out.println("Verified: they are equal");
        else System.out.println("Something is wrong: they are different");
    }
}
