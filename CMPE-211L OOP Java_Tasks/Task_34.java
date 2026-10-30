// Task_34: [oop]
// static block, instance block and constructor order
public class Task_34 {
    static class A {
        static { System.out.println("A: static block"); }
        { System.out.println("A: instance block"); }
        A() { System.out.println("A: constructor"); }
    }
    static class B extends A {
        static { System.out.println("B: static block"); }
        { System.out.println("B: instance block"); }
        B() { System.out.println("B: constructor"); }
    }
    public static void main(String[] args) {
        System.out.println("--- first new B() ---");
        new B();
        System.out.println("--- second new B() ---");
        new B();
        System.out.println("(static blocks run only once, the first time the class is used)");
    }
}
