import java.util.Scanner;
public class Task_01 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Exercise 01
        System.out.println("Anaya");

        // Exercise 02
        System.out.println("Enter your name:");
        String name = sc.nextLine();
        System.out.println("Enter your reg. no:");
        String regno = sc.nextLine();
        System.out.println("Your name:" + name);
        System.out.println("Your reg.no:" + regno);

        // Exercise 03
        System.out.println("Enter your minutes here:");
        int a = sc.nextInt();
        int h = a / 60;
        int m = a % 60;
        System.out.printf("%d:%02d\n", h, m);

        // Exercise 04
        System.out.print("Enter your minutes here:");
        int total = sc.nextInt();
        int hrs = (total / 60) % 12;
        int minutes = total % 60;
        System.out.printf("%d:%02d\n", hrs, minutes);

        sc.close();
    }
}
