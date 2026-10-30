// Task_27: [oop]
// Calculator with overloaded add() methods
public class Task_27 {
    static class Calculator {
        int add(int a, int b) {
            System.out.println("  add(int, int) was called");
            return a + b;
        }
        double add(double a, double b) {
            System.out.println("  add(double, double) was called");
            return a + b;
        }
        int add(int a, int b, int c) {
            System.out.println("  add(int, int, int) was called");
            return a + b + c;
        }
        String add(String a, String b) {
            System.out.println("  add(String, String) was called");
            return a + b;
        }
    }
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        System.out.println("add(5, 2.5)     -> " + calc.add(5, 2.5));
        System.out.println("add('a', 1)     -> " + calc.add('a', 1));
        System.out.println("add(\"5\", \"2\")   -> " + calc.add("5", "2"));
        System.out.println("add(1, 2, 3)    -> " + calc.add(1, 2, 3));
        System.out.println("add(3, 4)       -> " + calc.add(3, 4));
    }
}
