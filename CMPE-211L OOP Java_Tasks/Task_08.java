// Task_08: [oop]
// Counter with a static and an instance counter
public class Task_08 {
    static class Counter {
        private static int objectsCreated = 0;
        private int timesIncremented = 0;
        Counter() { objectsCreated++; }
        void increment() { timesIncremented++; }
        int getTimesIncremented() { return timesIncremented; }
        static int getObjectsCreated() { return objectsCreated; }
    }
    public static void main(String[] args) {
        Counter c1 = new Counter();
        Counter c2 = new Counter();
        Counter c3 = new Counter();
        c1.increment(); c1.increment();
        for (int i = 0; i < 5; i++) c2.increment();
        c3.increment();
        System.out.println("Objects created (static): " + Counter.getObjectsCreated());
        System.out.println("c1 incremented: " + c1.getTimesIncremented());
        System.out.println("c2 incremented: " + c2.getTimesIncremented());
        System.out.println("c3 incremented: " + c3.getTimesIncremented());
    }
}
