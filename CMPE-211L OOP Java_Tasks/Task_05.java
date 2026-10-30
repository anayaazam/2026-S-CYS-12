import java.util.Scanner;

// Task_05: [non_oop]
// number triangle 1, 22, 333, ...
public class Task_05 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter n: ");
        int n = sc.nextInt();
        for (int row = 1; row <= n; row++) {
            for (int count = 1; count <= row; count++) {
                System.out.print(row);
            }
            System.out.println();
        }
    }
}
