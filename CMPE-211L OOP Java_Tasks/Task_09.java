// Task_09: [non_oop]
// isPrime(n) loops only up to sqrt(n)
public class Task_09 {
    static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
    public static void main(String[] args) {
        System.out.println("Primes from 1 to 100:");
        for (int i = 1; i <= 100; i++) {
            if (isPrime(i)) System.out.print(i + " ");
        }
        System.out.println();
    }
}
