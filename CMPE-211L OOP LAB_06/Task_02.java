import java.util.Random;
import java.util.Scanner;

class Field {
    private int[][] hurdles = { {1, 2}, {-1, 1}, {2, -1}, {0, -3}, {-2, -2} };

    public boolean isHurdle(int x, int y) {
        for (int i = 0; i < hurdles.length; i++) {
            if (hurdles[i][0] == x && hurdles[i][1] == y) {
                return true;
            }
        }
        return false;
    }

    public String hurdleList() {
        String text = "";
        for (int i = 0; i < hurdles.length; i++) {
            text = text + "[" + hurdles[i][0] + ":" + hurdles[i][1] + "] ";
        }
        return text;
    }
}

class DirectedWalker {
    private String name;
    private int x = 0;
    private int y = 0;
    private Field field;

    public DirectedWalker(String name, Field field) {
        this.name = name;
        this.field = field;
    }

    public String where() {
        return x + " : " + y;
    }

    public boolean walk(String order) {
        if (order.equals("^")) {
            move(0, 1);
        } else if (order.equals("v")) {
            move(0, -1);
        } else if (order.equals("<")) {
            move(-1, 0);
        } else if (order.equals(">")) {
            move(1, 0);
        } else {
            return false;
        }
        return true;
    }

    private void move(int dx, int dy) {
        int newX = x + dx;
        int newY = y + dy;
        if (field.isHurdle(newX, newY)) {
            System.out.println(name + " encounters hurdle at [" + newX + ":" + newY + "]");
        } else {
            x = newX;
            y = newY;
        }
        System.out.println(name + " is at = " + where());
    }
}

class RandomWalker {
    private String name;
    private int x = 0;
    private int y = 0;
    private Field field;
    private Random random = new Random();

    public RandomWalker(String name, Field field) {
        this.name = name;
        this.field = field;
    }

    public String where() {
        return x + " : " + y;
    }

    public void walkRandomly() {
        int direction = random.nextInt(4);
        if (direction == 0) {
            move(0, 1);
        } else if (direction == 1) {
            move(0, -1);
        } else if (direction == 2) {
            move(-1, 0);
        } else {
            move(1, 0);
        }
    }

    private void move(int dx, int dy) {
        int newX = x + dx;
        int newY = y + dy;
        if (field.isHurdle(newX, newY)) {
            System.out.println(name + " encounters hurdle at [" + newX + ":" + newY + "]");
        } else {
            x = newX;
            y = newY;
        }
        System.out.println(name + " is at = " + where());
    }
}

public class Task_02 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        Field field = new Field();
        DirectedWalker ali = new DirectedWalker("Ali", field);
        RandomWalker hasan = new RandomWalker("Hasan", field);

        System.out.println("Hurdles are at: " + field.hurdleList());
        System.out.println("Starting: Ali's Location is = " + ali.where()
                + "  Hasan's Location is = " + hasan.where());
        System.out.println("Hasan has Random Movement, Ali follows order (^ v < >, q to quit)");

        while (true) {
            System.out.print("\nAli: Where should I go now: ");
            if (!sc.hasNextLine()) {
                break;
            }
            String order = sc.nextLine().trim();

            if (order.equals("q")) {
                System.out.println("Simulation finished.");
                break;
            }

            boolean ok = ali.walk(order);
            if (!ok) {
                System.out.println("Please type ^ v < > or q");
                continue;
            }
            hasan.walkRandomly();
        }
    }
}
