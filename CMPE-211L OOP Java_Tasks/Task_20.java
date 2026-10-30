// Task_20: [oop]
// abstract Shape, Circle, Triangle, polymorphism
public class Task_20 {
    static abstract class Shape {
        abstract double area();
    }
    static class Circle extends Shape {
        private double radius;
        Circle(double radius) { this.radius = radius; }
        double area() { return Math.PI * radius * radius; }
    }
    static class Triangle extends Shape {
        private double base, height;
        Triangle(double base, double height) { this.base = base; this.height = height; }
        double area() { return 0.5 * base * height; }
    }
    public static void main(String[] args) {
        Shape[] shapes = new Shape[4];
        shapes[0] = new Circle(2);
        shapes[1] = new Triangle(3, 4);
        shapes[2] = new Circle(1.5);
        shapes[3] = new Triangle(6, 2.5);
        double total = 0;
        for (int i = 0; i < shapes.length; i++) {
            System.out.printf("Shape %d area = %.2f%n", i + 1, shapes[i].area());
            total = total + shapes[i].area();
        }
        System.out.printf("Total area = %.2f%n", total);
    }
}
