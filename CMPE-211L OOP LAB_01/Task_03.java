import java.util.Scanner;
public class Task_03 {
    public static void main(String[] args) {
        // Exercise 15
        double pi = 3.99;
        int z = (int) pi;
        int w = (int) 7.9;
        System.out.println(z);
        System.out.println(w);

        // Exercise 16
        int number = Integer.parseInt("12");
        double gpa = Double.parseDouble("3.5");
        System.out.println(number);
        System.out.println(gpa);

        // Exercise 17
        var a = Math.pow(2, 10);
        System.out.println(a);

        // Exercise 18
        System.out.println(7 / 2);
        System.out.println(7 % 2);

        // Exercise 19
        System.out.println(Math.sqrt(16));
        System.out.println(Math.floor(3.7));
        System.out.println(Math.ceil(4.0));
        System.out.println(Math.abs(-5));
        System.out.println(Math.round(3.5));

        // Exercise 22
        Scanner sc = new Scanner(System.in);
        System.out.print("Your Name:");
        String name = sc.nextLine();
        System.out.println("Hello, " + name);
        sc.close();
    }
}
