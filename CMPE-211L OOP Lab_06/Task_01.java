class Counter {
    private int value;
    private int max;

    public Counter(int max) {
        this.max = max;
        value = 0;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int newValue) {
        value = newValue;
    }

    public void increment() {
        value = value + 1;
        if (value > max) {
            value = 0;
        }
    }
}

class DigitalTimer {
    private Counter hours = new Counter(23);
    private Counter minutes = new Counter(59);

    public DigitalTimer() {
    }

    public DigitalTimer(int h, int m) {
        set(h, m);
    }

    public void set(int h, int m) {
        if (h >= 0 && h <= 23 && m >= 0 && m <= 59) {
            hours.setValue(h);
            minutes.setValue(m);
        } else {
            System.out.println("Invalid time " + h + ":" + m);
        }
    }

    public void tick() {
        minutes.increment();
        if (minutes.getValue() == 0) {
            hours.increment();
        }
    }

    public String toString() {
        return String.format("%02d:%02d", hours.getValue(), minutes.getValue());
    }
}

public class Task_01 {
    public static void main(String[] args) {
        DigitalTimer t1 = new DigitalTimer();
        System.out.println("Default: " + t1);

        DigitalTimer t2 = new DigitalTimer(9, 30);
        System.out.println("Start: " + t2);
        t2.tick();
        System.out.println("After tick: " + t2);

        t2.set(23, 59);
        t2.tick();
        System.out.println("23:59 plus one minute: " + t2);

        t2.set(24, 10);
        t2.set(5, 60);
        System.out.println("Still: " + t2);
    }
}
