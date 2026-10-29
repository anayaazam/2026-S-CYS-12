import java.util.Random;
import java.util.Scanner;
public class Task_03 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Random random = new Random();
        Field field = new Field();
        Walker ali = new Walker("Ali");
        Walker hasan = new Walker("Hasan");
        System.out.println("Hurdles are at: " + field.hurdleList());
        System.out.println("Starting: Ali's Location is = " + ali.where()
                + "  Hasan's Location is = " + hasan.where());
        System.out.println("Hasan has random movement, Ali follows orders (^ v < >, q to quit)");
        while (true) {
            System.out.print("\nAli: Where should I go now: ");
            if (!sc.hasNextLine()) break;
            String order = sc.nextLine().trim();
            if (order.equals("q")) {
                System.out.println("Simulation finished.");
                break;
            }
            if (!(order.equals("^") || order.equals("v") || order.equals("<") || order.equals(">"))) {
                System.out.println("Please type ^ v < > or q");
                continue;
            }

            int dx = 0, dy = 0;
            if (order.equals("^")) dy = 1;
            if (order.equals("v")) dy = -1;
            if (order.equals("<")) dx = -1;
            if (order.equals(">")) dx = 1;
            ali.move(dx, dy, field);

            int direction = random.nextInt(4);
            dx = 0;
            dy = 0;
            if (direction == 0) dy = 1;
            if (direction == 1) dy = -1;
            if (direction == 2) dx = -1;
            if (direction == 3) dx = 1;
            hasan.move(dx, dy, field);
        }
    }
}
class Field {
    private int[][] hurdles = { {1, 2}, {-1, 1}, {2, -1}, {0, -3}, {-2, -2} };

    public boolean isHurdle(int x, int y) {
        for (int i = 0; i < hurdles.length; i++) {
            if (hurdles[i][0] == x && hurdles[i][1] == y) return true;
        }
        return false;
    }
    public String hurdleList() {
        String s = "";
        for (int i = 0; i < hurdles.length; i++) {
            s = s + "(" + hurdles[i][0] + " : " + hurdles[i][1] + ") ";
        }
        return s;
    }
}
class Walker {
    private String name;
    private int x = 0;
    private int y = 0;
    public Walker(String name) { this.name = name; }
    public String where() { return "(" + x + " : " + y + ")"; }
    public void move(int dx, int dy, Field field) {
        int newX = x + dx;
        int newY = y + dy;
        if (field.isHurdle(newX, newY)) {
            System.out.println(name + " encounters hurdle at (" + newX + ":" + newY + ")  "
                    + name + " is at = " + where());
        } else {
            x = newX;
            y = newY;
            System.out.println(name + " is at = " + where());
        }
    }
}
