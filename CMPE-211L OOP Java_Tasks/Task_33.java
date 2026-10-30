import java.util.Scanner;

// Task_33: [non_oop]
// all permutations of a String (recursion)
public class Task_33 {
    static Scanner sc = new Scanner(System.in);

    static void permute(String done, String left) {
        if (left.length() == 0) {
            System.out.println(done);
            return;
        }
        for (int i = 0; i < left.length(); i++) {
            String remaining = left.substring(0, i) + left.substring(i + 1);
            permute(done + left.charAt(i), remaining);
        }
    }
    public static void main(String[] args) {
        System.out.print("Enter a string with different characters: ");
        String text = sc.nextLine();
        permute("", text);
    }
}
