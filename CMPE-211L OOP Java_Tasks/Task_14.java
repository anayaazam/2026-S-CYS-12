import java.util.Arrays;

// Task_14: [non_oop]
// second largest value, no sorting
public class Task_14 {
    public static void main(String[] args) {
        int[] a = {12, 35, 1, 10, 34, 1, 35, 7, 35, 20};
        System.out.print("Array: ");
        System.out.println(Arrays.toString(a));
        int largest = a[0];
        boolean foundSecond = false;
        int second = 0;
        for (int i = 1; i < a.length; i++) {
            if (a[i] > largest) {
                second = largest;
                foundSecond = true;
                largest = a[i];
            } else if (a[i] < largest && (!foundSecond || a[i] > second)) {
                second = a[i];
                foundSecond = true;
            }
        }
        if (foundSecond) {
            System.out.println("Largest = " + largest + ", second largest = " + second);
        } else {
            System.out.println("There is no second largest (all values are equal)");
        }
    }
}
