import java.util.Scanner;

// Task_18: [non_oop]
// anagram check without sorting
public class Task_18 {
    static Scanner sc = new Scanner(System.in);

    static boolean areAnagrams(String a, String b) {
        a = a.toLowerCase();
        b = b.toLowerCase();
        int[] count = new int[26];
        for (int i = 0; i < a.length(); i++) {
            char ch = a.charAt(i);
            if (ch >= 'a' && ch <= 'z') count[ch - 'a']++;
        }
        for (int i = 0; i < b.length(); i++) {
            char ch = b.charAt(i);
            if (ch >= 'a' && ch <= 'z') count[ch - 'a']--;
        }
        for (int i = 0; i < 26; i++) {
            if (count[i] != 0) return false;
        }
        return true;
    }
    public static void main(String[] args) {
        System.out.print("First string: ");
        String a = sc.nextLine();
        System.out.print("Second string: ");
        String b = sc.nextLine();
        if (areAnagrams(a, b)) {
            System.out.println("They are anagrams");
        } else {
            System.out.println("They are NOT anagrams");
        }
    }
}
