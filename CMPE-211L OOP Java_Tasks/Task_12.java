import java.util.Scanner;

// Task_12: [non_oop]
// palindrome ignoring case, spaces and punctuation
public class Task_12 {
    static Scanner sc = new Scanner(System.in);

    static boolean isPalindrome(String text) {
        String clean = "";
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            if (Character.isLetterOrDigit(ch)) {
                clean = clean + Character.toLowerCase(ch);
            }
        }
        int left = 0;
        int right = clean.length() - 1;
        while (left < right) {
            if (clean.charAt(left) != clean.charAt(right)) return false;
            left++;
            right--;
        }
        return true;
    }
    public static void main(String[] args) {
        System.out.print("Enter a string: ");
        String text = sc.nextLine();
        System.out.println(isPalindrome(text));
    }
}
