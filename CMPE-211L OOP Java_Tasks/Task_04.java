// Task_04: [oop]
// Rectangle class
public class Task_04 {
    static class Rectangle {
        private double width;
        private double height;

        Rectangle(double width, double height) {
            this.width = width;
            this.height = height;
        }
        double area() { return width * height; }
        double perimeter() { return 2 * (width + height); }
        boolean isSquare() { return width == height; }

        public String toString() { return "Rectangle " + width + " x " + height; }
    }
    public static void main(String[] args) {
        Rectangle r1 = new Rectangle(5, 4);
        Rectangle r2 = new Rectangle(6, 6);
        System.out.println(r1 + ": area=" + r1.area() + ", perimeter=" + r1.perimeter()
                + ", square? " + r1.isSquare());
        System.out.println(r2 + ": area=" + r2.area() + ", perimeter=" + r2.perimeter()
                + ", square? " + r2.isSquare());

        if (r1.area() > r2.area()) {
            System.out.println("Larger area: " + r1);
        } else if (r2.area() > r1.area()) {
            System.out.println("Larger area: " + r2);
        } else {
            System.out.println("Both have the same area");
        }
    }
}
