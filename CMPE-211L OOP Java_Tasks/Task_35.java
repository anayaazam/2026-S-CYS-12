import java.util.Arrays;
import java.util.Scanner;

// Task_35: [non_oop]
// iterative binary search with step count
public class Task_35 {
    static Scanner sc = new Scanner(System.in);

    static int steps = 0;
    static int binarySearch(int[] a, int key) {
        steps = 0;
        int low = 0, high = a.length - 1;
        while (low <= high) {
            steps++;
            int mid = (low + high) / 2;
            if (a[mid] == key) return mid;
            if (a[mid] < key) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
    static int firstOccurrence(int[] a, int key) {
        steps = 0;
        int low = 0, high = a.length - 1;
        int answer = -1;
        while (low <= high) {
            steps++;
            int mid = (low + high) / 2;
            if (a[mid] == key) {
                answer = mid;
                high = mid - 1;
            } else if (a[mid] < key) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return answer;
    }
    public static void main(String[] args) {
        int[] sorted = {1, 3, 5, 7, 9, 11, 13, 15};
        int[] withDuplicates = {2, 4, 4, 4, 4, 7, 9, 9};
        System.out.print("Number to search for: ");
        int key = sc.nextInt();
        System.out.print("Array 1: ");
        System.out.println(Arrays.toString(sorted));
        int index = binarySearch(sorted, key);
        System.out.println("binarySearch -> index " + index + " in " + steps + " step(s)");
        System.out.print("Array 2: ");
        System.out.println(Arrays.toString(withDuplicates));
        index = firstOccurrence(withDuplicates, key);
        System.out.println("firstOccurrence -> index " + index + " in " + steps + " step(s)");
    }
}
