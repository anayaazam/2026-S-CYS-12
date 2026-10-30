import java.util.Arrays;

// Task_30: [non_oop]
// missing number in 1..n (no sorting, no extra array)
public class Task_30 {
    public static void main(String[] args) {
        int[] a = {1, 2, 4, 5, 6, 3, 8, 9, 10};
        int n = a.length + 1;
        System.out.print("Array: ");
        System.out.println(Arrays.toString(a));
        int expectedSum = n * (n + 1) / 2;
        int actualSum = 0;
        for (int i = 0; i < a.length; i++) actualSum = actualSum + a[i];
        System.out.println("Missing number: " + (expectedSum - actualSum));
    }
}
