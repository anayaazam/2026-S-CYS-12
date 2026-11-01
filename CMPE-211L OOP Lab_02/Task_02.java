import java.util.Scanner;
public class Task_02 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[] arr = {2, 4, 5, 3, 6, 32, 78, 6, 54, 9, 8, 12};

        // Exercise 05
        System.out.print("Enter your start here:");
        int s = sc.nextInt();
        System.out.print("Enter your end here:");
        int e = sc.nextInt();
        System.out.print("Enter your increment here:");
        int inc = sc.nextInt();

        for (int i = s; i < e && i < arr.length; i += inc) {
            System.out.println(arr[i]);
        }

        sc.close();
    }
}
