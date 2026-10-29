public class Task_01 {
    public static void main(String[] args) {
        JTime t1 = new JTime(8, 30, 15);
        JTime t2 = new JTime(14, 45, 50);
        JTime midnight = new JTime();
        JTime copyOfT1 = new JTime(t1);
        System.out.println("t1       = " + t1);
        System.out.println("t2       = " + t2);
        System.out.println("midnight = " + midnight);
        System.out.println("copy of t1 = " + copyOfT1);
        System.out.println();
        System.out.println("a) elapsed time in seconds");
        System.out.println("Between t1 and t2: " + t1.secondsBetween(t2) + " seconds");
        System.out.println("Between t2 and t1: " + t2.secondsBetween(t1) + " seconds (same, order does not matter)");
        System.out.println();
        System.out.println("b) elapsed time as another time-stamp");
        JTime gap = t1.timeBetween(t2);
        System.out.println("Between t1 and t2: " + gap + "  (" + gap.getHour() + " h "
                + gap.getMinute() + " m " + gap.getSecond() + " s)");
        System.out.println();
        System.out.println("c) constructor from seconds after 12 am");
        JTime fromSeconds1 = new JTime(3725);
        JTime fromSeconds2 = new JTime(45296);
        JTime fromSeconds3 = new JTime(86399);
        JTime fromSeconds4 = new JTime(86405);
        System.out.println("3725 seconds   -> " + fromSeconds1);
        System.out.println("45296 seconds  -> " + fromSeconds2);
        System.out.println("86399 seconds  -> " + fromSeconds3);
        System.out.println("86405 seconds  -> " + fromSeconds4 + "  (wrapped past midnight)");
        System.out.println();
        System.out.println("extra: invalid values are rejected");
        JTime bad = new JTime(25, 61, 70);
        System.out.println("bad = " + bad);
    }
}
class JTime {
    private int hour;
    private int minute;
    private int second;
    public JTime() {
        hour = 0;
        minute = 0;
        second = 0;
    }
    public JTime(int hour, int minute, int second) {
        setHour(hour);
        setMinute(minute);
        setSecond(second);
    }
    public JTime(JTime other) {
        hour = other.hour;
        minute = other.minute;
        second = other.second;
    }
    public JTime(int totalSeconds) {
        if (totalSeconds < 0) {
            System.out.println("Invalid number of seconds: " + totalSeconds + " (using 00:00:00)");
            return;
        }
        totalSeconds = totalSeconds % 86400;
        hour = totalSeconds / 3600;
        minute = (totalSeconds % 3600) / 60;
        second = totalSeconds % 60;
    }
    public int getHour()   { return hour; }
    public int getMinute() { return minute; }
    public int getSecond() { return second; }
    public void setHour(int hour) {
        if (hour >= 0 && hour <= 23) this.hour = hour;
        else System.out.println("Invalid hour: " + hour + " (must be 0-23)");
    }
    public void setMinute(int minute) {
        if (minute >= 0 && minute <= 59) this.minute = minute;
        else System.out.println("Invalid minute: " + minute + " (must be 0-59)");
    }
    public void setSecond(int second) {
        if (second >= 0 && second <= 59) this.second = second;
        else System.out.println("Invalid second: " + second + " (must be 0-59)");
    }
    public int toSeconds() {
        return hour * 3600 + minute * 60 + second;
    }
    public int secondsBetween(JTime other) {
        int difference = this.toSeconds() - other.toSeconds();
        if (difference < 0) difference = -difference;
        return difference;
    }
    public JTime timeBetween(JTime other) {
        return new JTime(secondsBetween(other));
    }
    public String toString() {
        return String.format("%02d:%02d:%02d", hour, minute, second);
    }
}
