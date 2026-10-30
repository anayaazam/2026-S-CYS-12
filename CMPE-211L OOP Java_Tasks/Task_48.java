// Task_48: [non_oop]
// validate a 9x9 Sudoku grid
public class Task_48 {
    static boolean isValidSudoku(int[][] g) {
        for (int row = 0; row < 9; row++) {
            boolean[] seen = new boolean[10];
            for (int col = 0; col < 9; col++) {
                int v = g[row][col];
                if (v < 1 || v > 9 || seen[v]) return false;
                seen[v] = true;
            }
        }
        for (int col = 0; col < 9; col++) {
            boolean[] seen = new boolean[10];
            for (int row = 0; row < 9; row++) {
                int v = g[row][col];
                if (v < 1 || v > 9 || seen[v]) return false;
                seen[v] = true;
            }
        }
        for (int boxRow = 0; boxRow < 9; boxRow += 3) {
            for (int boxCol = 0; boxCol < 9; boxCol += 3) {
                boolean[] seen = new boolean[10];
                for (int r = 0; r < 3; r++) {
                    for (int c = 0; c < 3; c++) {
                        int v = g[boxRow + r][boxCol + c];
                        if (v < 1 || v > 9 || seen[v]) return false;
                        seen[v] = true;
                    }
                }
            }
        }
        return true;
    }
    public static void main(String[] args) {
        int[][] grid = {
            {5, 3, 4, 6, 7, 8, 9, 1, 2},
            {6, 7, 2, 1, 9, 5, 3, 4, 8},
            {1, 9, 8, 3, 4, 2, 5, 6, 7},
            {8, 5, 9, 7, 6, 1, 4, 2, 3},
            {4, 2, 6, 8, 5, 3, 7, 9, 1},
            {7, 1, 3, 9, 2, 4, 8, 5, 6},
            {9, 6, 1, 5, 3, 7, 2, 8, 4},
            {2, 8, 7, 4, 1, 9, 6, 3, 5},
            {3, 4, 5, 2, 8, 6, 1, 7, 9}
        };
        System.out.println("Correct grid valid?   " + isValidSudoku(grid));
        grid[0][0] = 3;
        System.out.println("Changed grid valid?   " + isValidSudoku(grid));
    }
}
