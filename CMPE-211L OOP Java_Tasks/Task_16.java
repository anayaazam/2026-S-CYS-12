import java.util.Scanner;

// Task_16: [non_oop]
// hollow diamond of stars (odd n)
public class Task_16 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter an odd number: ");
        int n = sc.nextInt();
        if (n < 1 || n / 2 * 2 == n) {
            System.out.println("n must be a positive odd number");
            return;
        }
        int middle = n / 2;
        for (int row = 0; row < n; row++) {
            int outer = Math.abs(middle - row);
            int inner = n - 2 * outer - 2;
            for (int i = 0; i < outer; i++) System.out.print(" ");
            System.out.print("*");
            if (inner >= 0) {
                for (int i = 0; i < inner; i++) System.out.print(" ");
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
