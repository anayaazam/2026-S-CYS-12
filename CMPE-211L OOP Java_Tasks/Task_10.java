import java.util.Scanner;

// Task_10: [non_oop]
// count vowels, consonants, digits, others (one loop)
public class Task_10 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter a string: ");
        String text = sc.nextLine();
        int vowels = 0, consonants = 0, digits = 0, others = 0;

        for (int i = 0; i < text.length(); i++) {
            char ch = Character.toLowerCase(text.charAt(i));
            if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
                vowels++;
            } else if (ch >= 'a' && ch <= 'z') {
                consonants++;
            } else if (ch >= '0' && ch <= '9') {
                digits++;
            } else {
                others++;
            }
        }
        System.out.println("Vowels: " + vowels + ", Consonants: " + consonants
                + ", Digits: " + digits + ", Others: " + others);
    }
}
