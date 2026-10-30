import java.util.Arrays;

// Task_42: [non_oop]
// merge two sorted arrays in O(n + m)
public class Task_42 {
    public static void main(String[] args) {
        int[] a = {1, 4, 7, 10, 15};
        int[] b = {2, 3, 8, 9, 20, 25};
        int[] merged = new int[a.length + b.length];
        int i = 0, j = 0, k = 0;
        while (i < a.length && j < b.length) {
            if (a[i] <= b[j]) {
                merged[k] = a[i];
                i++;
            } else {
                merged[k] = b[j];
                j++;
            }
            k++;
        }
        while (i < a.length) { merged[k] = a[i]; i++; k++; }
        while (j < b.length) { merged[k] = b[j]; j++; k++; }
        System.out.print("a:      "); System.out.println(Arrays.toString(a));
        System.out.print("b:      "); System.out.println(Arrays.toString(b));
        System.out.print("merged: "); System.out.println(Arrays.toString(merged));
    }
}
