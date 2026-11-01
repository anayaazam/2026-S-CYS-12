import java.util.Scanner;
class place {
    String[][] shelves;
    int[] bookCount;
    place() {
        shelves = new String[5][5];
        bookCount = new int[5];
    }
    void placeBook(String book, int shelf) {
        if (shelf < 1 || shelf > 5) {
            System.out.println("Shelf does not exist");
            return;
        }
        int row = shelf - 1;
        if (bookCount[row] == 5) {
            System.out.println("Shelf " + shelf + " is full");
            return;
        }
        shelves[row][bookCount[row]] = book;
        bookCount[row]++;
    }
    void showShelves() {
        System.out.println("\n Shelves");
        for (int i = 0; i < 5; i++) {
            System.out.print("Shelf " + (i + 1) + ": ");
            if (bookCount[i] == 0) {
                System.out.print("(empty)");
            }
            for (int j = 0; j < bookCount[i]; j++) {
                System.out.print(shelves[i][j] + "  ");
            }
            System.out.println();
        }
    }
}
public class Task_05 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        place p = new place();
        System.out.println("How many books do you want to place?");
        int num = sc.nextInt();
        sc.nextLine();
        for (int i = 1; i <= num; i++) {
            System.out.print("Enter your book name: ");
            String book = sc.nextLine();
            System.out.println("Enter the shelf place(1-5):");
            int shelf = sc.nextInt();
            sc.nextLine();
            p.placeBook(book, shelf);
        }
        p.showShelves();
    }
}
