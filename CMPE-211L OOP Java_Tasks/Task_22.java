import java.util.Scanner;

// Task_22: [non_oop]
// 3x3 matrix, transpose, symmetric?
public class Task_22 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        int[][] m = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print("Enter element [" + i + "][" + j + "]: ");
                m[i][j] = sc.nextInt();
            }
        }
        System.out.println("Matrix:");
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) System.out.print(m[i][j] + "\t");
            System.out.println();
        }
        System.out.println("Transpose:");
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) System.out.print(m[j][i] + "\t");
            System.out.println();
        }
        boolean symmetric = true;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (m[i][j] != m[j][i]) symmetric = false;
            }
        }
        if (symmetric) {
            System.out.println("The matrix is symmetric");
        } else {
            System.out.println("The matrix is NOT symmetric");
        }
    }
}
