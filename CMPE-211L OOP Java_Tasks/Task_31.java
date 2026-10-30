import java.util.Scanner;

// Task_31: [non_oop]
// Pascal's triangle with a jagged 2D array
public class Task_31 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("How many rows? ");
        int n = sc.nextInt();
        int[][] triangle = new int[n][];
        for (int i = 0; i < n; i++) {
            triangle[i] = new int[i + 1];
            triangle[i][0] = 1;
            triangle[i][i] = 1;
            for (int j = 1; j < i; j++) {
                triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
            }
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j <= i; j++) System.out.print(triangle[i][j] + " ");
            System.out.println();
        }
    }
}
