import java.util.Scanner;

// Task_24: [oop]
// Point class, right-angled triangle?
public class Task_24 {
    static Scanner sc = new Scanner(System.in);

    static class Point {
        private double x, y;
        Point(double x, double y) { this.x = x; this.y = y; }
        double getX() { return x; }
        double getY() { return y; }
        double distanceTo(Point p) {
            double dx = x - p.x;
            double dy = y - p.y;
            return Math.sqrt(dx * dx + dy * dy);
        }
    }
    public static void main(String[] args) {
        Point[] p = new Point[3];
        for (int i = 0; i < 3; i++) {
            System.out.print("Point " + (i + 1) + " x: ");
            double x = sc.nextDouble();
            System.out.print("Point " + (i + 1) + " y: ");
            double y = sc.nextDouble();
            p[i] = new Point(x, y);
        }
        double cross = (p[1].getX() - p[0].getX()) * (p[2].getY() - p[0].getY())
                     - (p[2].getX() - p[0].getX()) * (p[1].getY() - p[0].getY());
        if (Math.abs(cross) < 0.000001) {
            System.out.println("These points do not form a triangle");
            return;
        }
        double a = p[0].distanceTo(p[1]);
        double b = p[1].distanceTo(p[2]);
        double c = p[2].distanceTo(p[0]);
        boolean right = Math.abs(a * a + b * b - c * c) < 0.000001
                     || Math.abs(b * b + c * c - a * a) < 0.000001
                     || Math.abs(a * a + c * c - b * b) < 0.000001;
        if (right) {
            System.out.println("It IS a right-angled triangle");
        } else {
            System.out.println("It is NOT a right-angled triangle");
        }
    }
}
