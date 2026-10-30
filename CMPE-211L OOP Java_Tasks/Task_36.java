import java.util.Scanner;

// Task_36: [non_oop]
// longest substring without repeating characters
public class Task_36 {
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.print("Enter a string: ");
        String s = sc.nextLine();
        String best = "";
        for (int start = 0; start < s.length(); start++) {
            for (int end = start; end < s.length(); end++) {
                boolean repeated = false;
                for (int k = start; k < end; k++) {
                    if (s.charAt(k) == s.charAt(end)) repeated = true;
                }
                if (repeated) break;
                if (end - start + 1 > best.length()) {
                    best = s.substring(start, end + 1);
                }
            }
        }
        System.out.println("Longest substring: \"" + best + "\"");
        System.out.println("Length: " + best.length());
    }
}
