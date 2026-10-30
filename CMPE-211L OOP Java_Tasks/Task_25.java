import java.util.Scanner;

// Task_25: [non_oop]
// first non-repeating character
public class Task_25 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter a string: ");
        String text = sc.nextLine();
        for (int i = 0; i < text.length(); i++) {
            boolean repeats = false;
            for (int j = 0; j < text.length(); j++) {
                if (i != j && text.charAt(i) == text.charAt(j)) repeats = true;
            }
            if (!repeats) {
                System.out.println("First non-repeating character: " + text.charAt(i));
                return;
            }
        }
        System.out.println("none");
    }
}
