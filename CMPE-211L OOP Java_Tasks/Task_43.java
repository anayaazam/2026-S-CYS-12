// Task_43: [oop]
// Singleton, lazy initialisation, then thread-safe
public class Task_43 {

    static class LazySingleton {
        private static LazySingleton instance;

        private LazySingleton() {
            System.out.println("  (creating the instance)");
        }
        static LazySingleton getInstance() {
            if (instance == null) {
                instance = new LazySingleton();
            }
            return instance;
        }
    }

    static class SafeSingleton {
        private static SafeSingleton instance;

        private SafeSingleton() {
            System.out.println("  (creating the safe instance)");
        }

        static synchronized SafeSingleton getInstance() {
            if (instance == null) {
                instance = new SafeSingleton();
            }
            return instance;
        }
    }
    static class Worker extends Thread {
        private SafeSingleton first;
        Worker(SafeSingleton first) { this.first = first; }

        public void run() {
            SafeSingleton s = SafeSingleton.getInstance();
            System.out.println("  thread got the same instance? " + (s == first));
        }
    }
    public static void main(String[] args) {
        System.out.println("Lazy singleton, 5 calls:");
        LazySingleton first = LazySingleton.getInstance();
        for (int i = 1; i <= 5; i++) {
            LazySingleton s = LazySingleton.getInstance();
            System.out.println("  call " + i + ": same instance as first? " + (s == first));
        }
        System.out.println("Thread-safe singleton, 5 threads:");
        SafeSingleton safeFirst = SafeSingleton.getInstance();
        Worker[] workers = new Worker[5];
        for (int i = 0; i < 5; i++) {
            workers[i] = new Worker(safeFirst);
            workers[i].start();
        }
        for (int i = 0; i < 5; i++) {
            try {
                workers[i].join();
            } catch (InterruptedException e) {
                System.out.println("Interrupted");
            }
        }
    }
}
