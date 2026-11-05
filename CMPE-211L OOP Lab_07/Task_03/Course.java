package Courses;
public class Course {
    String name;
    Student[] students = new Student[10];
    int studentCount = 0;
    Course(String name) {
        this.name = name;
    }
    boolean isFull() {
        return studentCount == students.length;
    }
    void addStudent(Student student) {
        students[studentCount] = student;
        studentCount++;
    }
    void enroll(Student student) {
        student.enroll(this);
    }
    void showStudents() {
        System.out.print(name + " has: ");
        for (int i = 0; i < studentCount; i++) {
            System.out.print(students[i].name + " ");
        }
        System.out.println();
    }
    @Override
    public String toString() {
        return name;
    }
}
