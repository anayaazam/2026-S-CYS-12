// Task_44: [non_oop]
// N-Queens for N = 6
public class Task_44 {
    static int N = 6;
    static int[] queenColumn = new int[N];
    static int[] firstBoard = null;
    static int solutionCount = 0;
    static boolean isSafe(int row, int col) {
        for (int r = 0; r < row; r++) {
            if (queenColumn[r] == col) return false;
            if (Math.abs(queenColumn[r] - col) == row - r) return false;
        }
        return true;
    }
    static void placeQueen(int row) {
        if (row == N) {
            solutionCount++;
            if (solutionCount == 1) {
                firstBoard = new int[N];
                for (int i = 0; i < N; i++) firstBoard[i] = queenColumn[i];
            }
            return;
        }
        for (int col = 0; col < N; col++) {
            if (isSafe(row, col)) {
                queenColumn[row] = col;
                placeQueen(row + 1);
            }
        }
    }
    public static void main(String[] args) {
        solutionCount = 0;
        firstBoard = null;
        placeQueen(0);
        System.out.println("Total solutions for N = " + N + ": " + solutionCount);
        System.out.println("One valid board:");
        for (int row = 0; row < N; row++) {
            for (int col = 0; col < N; col++) {
                if (firstBoard[row] == col) System.out.print("Q ");
                else System.out.print(". ");
            }
            System.out.println();
        }
    }
}
