import java.util.Scanner;
class dayType {
    private String[] days = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
    private int currentDay;
    public dayType() {
        currentDay = 0;
    }
    public void setDay(String day) {
        for (int i = 0; i < 7; i++) {
            if (days[i].equalsIgnoreCase(day)) {
                currentDay = i;
            }
        }
    }
    public void printDay() {
        System.out.println("The day is " + days[currentDay]);
    }
    public String getDay() {
        return days[currentDay];
    }
    public String nextDay() {
        int next = currentDay + 1;
        if (next == 7) {
            next = 0;
        }
        return days[next];
    }
    public String previousDay() {
        int previous = currentDay - 1;
        if (previous == -1) {
            previous = 6;
        }
        return days[previous];
    }
    public String addDays(int numberOfDays) {
        int newDay = (currentDay + numberOfDays) % 7;
        if (newDay < 0) {
            newDay = newDay + 7;
        }
        return days[newDay];
    }
}
public class Task_01 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        dayType today = new dayType();
        System.out.print("Enter the day (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ");
        String day = input.next();
        today.setDay(day);
        today.printDay();
        System.out.println("Current day: " + today.getDay());
        System.out.println("Next day: " + today.nextDay());
        System.out.println("Previous day: " + today.previousDay());
        System.out.print("Enter number of days to add: ");
        int numberOfDays = input.nextInt();
        System.out.println("Day after adding " + numberOfDays + " days: " + today.addDays(numberOfDays));
    }
}
