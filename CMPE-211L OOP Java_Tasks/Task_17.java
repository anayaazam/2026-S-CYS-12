// Task_17: [oop]
// Student with marks, average() and grade()
public class Task_17 {
    static class Student {
        private String name;
        private int[] marks;
        Student(String name, int[] marks) {
            this.name = name;
            this.marks = marks;
        }
        String getName() { return name; }
        double average() {
            if (marks.length == 0) return 0;
            int sum = 0;
            for (int i = 0; i < marks.length; i++) sum = sum + marks[i];
            return (double) sum / marks.length;
        }
        String grade() {
            double avg = average();
            if (avg >= 90) return "A";
            if (avg >= 80) return "B";
            if (avg >= 70) return "C";
            if (avg >= 60) return "D";
            return "F";
        }
    }
    public static void main(String[] args) {
        Student[] students = new Student[3];
        students[0] = new Student("Ali", new int[]{80, 90, 70});
        students[1] = new Student("Sara", new int[]{95, 92, 98});
        students[2] = new Student("Omar", new int[]{60, 55, 65});
        Student topper = students[0];
        for (int i = 0; i < students.length; i++) {
            Student s = students[i];
            System.out.printf("%s: average = %.2f, grade = %s%n", s.getName(), s.average(), s.grade());
            if (s.average() > topper.average()) topper = s;
        }
        System.out.println("Topper: " + topper.getName());
    }
}
