import java.util.Scanner;

// Task_23: [non_oop]
// decimal to binary, with a loop and with recursion
public class Task_23 {
    static Scanner sc = new Scanner(System.in);

    static String binaryWithLoop(int n) {
        if (n == 0) return "0";
        String result = "";
        while (n > 0) {
            result = (n % 2) + result;
            n = n / 2;
        }
        return result;
    }
    static String binaryWithRecursion(int n) {
        if (n < 2) return "" + n;
        return binaryWithRecursion(n / 2) + (n % 2);
    }
    public static void main(String[] args) {
        System.out.print("Enter a decimal number: ");
        int n = sc.nextInt();
        String sign = "";
        if (n < 0) {
            sign = "-";
            n = -n;
        }
        System.out.println("Loop:      " + sign + binaryWithLoop(n));
        System.out.println("Recursion: " + sign + binaryWithRecursion(n));
    }
}
