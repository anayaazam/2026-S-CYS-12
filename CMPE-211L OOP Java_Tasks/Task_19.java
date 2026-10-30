import java.util.Arrays;

// Task_19: [non_oop]
// remove duplicates, keep the order, no Collections
public class Task_19 {
    public static void main(String[] args) {
        int[] a = {4, 5, 4, 2, 5, 9, 2, 1, 9};
        System.out.print("Original: ");
        System.out.println(Arrays.toString(a));
        int[] result = new int[a.length];
        int size = 0;
        for (int i = 0; i < a.length; i++) {
            boolean alreadyThere = false;
            for (int j = 0; j < size; j++) {
                if (result[j] == a[i]) alreadyThere = true;
            }
            if (!alreadyThere) {
                result[size] = a[i];
                size++;
            }
        }
        System.out.print("Result:   ");
        for (int i = 0; i < size; i++) System.out.print(result[i] + " ");
        System.out.println();
    }
}
