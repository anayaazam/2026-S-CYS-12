// Task_47: [oop]
// generic Pair<K, V> and generic max()
public class Task_47 {
    static class Pair<K, V> {
        private K key;
        private V value;
        Pair(K key, V value) { this.key = key; this.value = value; }
        K getKey() { return key; }
        V getValue() { return value; }
        public String toString() { return "(" + key + ", " + value + ")"; }
    }
    static class Student implements Comparable<Student> {
        private String name;
        private int marks;
        Student(String name, int marks) { this.name = name; this.marks = marks; }
        public int compareTo(Student other) {
            return Integer.compare(marks, other.marks);
        }
        public String toString() { return name + " (" + marks + ")"; }
    }
    static <T extends Comparable<T>> T max(T[] items) {
        T biggest = items[0];
        for (int i = 1; i < items.length; i++) {
            if (items[i].compareTo(biggest) > 0) biggest = items[i];
        }
        return biggest;
    }
    public static void main(String[] args) {
        Pair<String, Integer> pair = new Pair<>("age", 20);
        System.out.println("Pair: " + pair + "  key=" + pair.getKey() + "  value=" + pair.getValue());
        Integer[] numbers = {3, 9, 4, 7};
        String[] words = {"pear", "apple", "zebra", "mango"};
        Student[] students = {new Student("Ali", 80), new Student("Sara", 95), new Student("Omar", 60)};
        System.out.println("max of Integers: " + max(numbers));
        System.out.println("max of Strings:  " + max(words));
        System.out.println("max of Students: " + max(students));
    }
}
