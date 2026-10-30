// Task_45: [oop]
// two interfaces with the same default method
public class Task_45 {
    interface A {
        default void hello() {
            System.out.println("Hello from A"); }
    }
    interface B {
        default void hello() {
            System.out.println("Hello from B"); }
    }
    static class C implements A, B {
        public void hello() {
            A.super.hello();
            B.super.hello();
        }
    }
    public static void main(String[] args) {
        new C().hello();
    }
}
