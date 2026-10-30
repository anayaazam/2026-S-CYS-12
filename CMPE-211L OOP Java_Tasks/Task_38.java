import java.util.Scanner;

// Task_38: [non_oop]
// print an n x m matrix in spiral order
public class Task_38 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Rows (n): ");
        int rows = sc.nextInt();
        System.out.print("Columns (m): ");
        int cols = sc.nextInt();
        int[][] m = new int[rows][cols];
        int value = 1;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                m[i][j] = value;
                value++;
            }
        }
        System.out.println("Matrix:");
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) System.out.print(m[i][j] + "\t");
            System.out.println();
        }
        int top = 0, bottom = rows - 1, left = 0, right = cols - 1;
        System.out.print("Spiral: ");
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) System.out.print(m[top][j] + " ");
            top++;
            for (int i = top; i <= bottom; i++) System.out.print(m[i][right] + " ");
            right--;
            if (top <= bottom) {
                for (int j = right; j >= left; j--) System.out.print(m[bottom][j] + " ");
                bottom--;
            }
            if (left <= right) {
                for (int i = bottom; i >= top; i--) System.out.print(m[i][left] + " ");
                left++;
            }
        }
        System.out.println();
    }
}
