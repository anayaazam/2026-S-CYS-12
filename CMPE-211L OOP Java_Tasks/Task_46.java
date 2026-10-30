import java.util.Arrays;

// Task_46: [non_oop]
// Kadane's algorithm (maximum subarray)
public class Task_46 {
    static void kadane(int[] a) {
        int best = a[0];
        int bestStart = 0, bestEnd = 0;
        int current = a[0];
        int currentStart = 0;
        for (int i = 1; i < a.length; i++) {
            if (current < 0) {
                current = a[i];
                currentStart = i;
            } else {
                current = current + a[i];
            }
            if (current > best) {
                best = current;
                bestStart = currentStart;
                bestEnd = i;
            }
        }
        System.out.print("Array: ");
        System.out.println(Arrays.toString(a));
        System.out.println("Max sum = " + best + " (from index " + bestStart + " to " + bestEnd + ")");
    }
    public static void main(String[] args) {
        kadane(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4});
        kadane(new int[]{-8, -3, -6, -2, -5});
    }
}
