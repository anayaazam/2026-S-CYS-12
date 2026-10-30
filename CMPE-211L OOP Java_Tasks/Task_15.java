import java.util.Arrays;
import java.util.Scanner;

// Task_15: [non_oop]
// rotate an array left by k, in place
public class Task_15 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        int[] a = {1, 2, 3, 4, 5, 6, 7};
        System.out.print("Rotate left by k = ");
        int k = sc.nextInt();
        System.out.print("Before: ");
        System.out.println(Arrays.toString(a));
        int n = a.length;
        k = k % n;
        if (k < 0) k = k + n;
        for (int step = 0; step < k; step++) {
            int first = a[0];
            for (int i = 0; i < n - 1; i++) {
                a[i] = a[i + 1];
            }
            a[n - 1] = first;
        }
        System.out.print("After:  ");
        System.out.println(Arrays.toString(a));
    }
}
