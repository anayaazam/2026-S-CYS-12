import java.util.Scanner;

// Task_28: [non_oop]
// compress "aaabbc" -> "a3b2c1" and decompress
public class Task_28 {
    static Scanner sc = new Scanner(System.in);

    static String compress(String s) {
        if (s.length() == 0) return "";
        String result = "";
        char current = s.charAt(0);
        int count = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == current) {
                count++;
            } else {
                result = result + current + count;
                current = s.charAt(i);
                count = 1;
            }
        }
        result = result + current + count;
        return result;
    }
    static String decompress(String s) {
        String result = "";
        int i = 0;
        while (i < s.length()) {
            char letter = s.charAt(i);
            i++;
            int count = 0;
            while (i < s.length() && Character.isDigit(s.charAt(i))) {
                count = count * 10 + (s.charAt(i) - '0');
                i++;
            }
            for (int k = 0; k < count; k++) result = result + letter;
        }
        return result;
    }
    public static void main(String[] args) {
        System.out.print("Enter a string (letters only, e.g. aaabbc): ");
        String text = sc.nextLine();
        String packed = compress(text);
        System.out.println("Compressed:   " + packed);
        System.out.println("Decompressed: " + decompress(packed));
    }
}
