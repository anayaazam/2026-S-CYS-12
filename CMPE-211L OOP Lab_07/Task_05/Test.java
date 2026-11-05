package Courses;
public class Test {
    public static void main(String[] args) {
        Student anaya = new Student("Anaya");
        Student fizza = new Student("Fizza");
        Student ushna = new Student("Ushna");
        Student fatima = new Student("Fatima");
        Course db = new Course("DB");
        Course oop = new Course("OOP");
        Course dld = new Course("DLD");
        Course mvc = new Course("MVC");
        anaya.enroll(db);
        anaya.enroll(oop);
        anaya.enroll(dld);
        fizza.enroll(db);
        fizza.enroll(mvc);
        ushna.enroll(oop);
        ushna.enroll(dld);
        ushna.enroll(mvc);
        fatima.enroll(db);
        fatima.enroll(oop);
        dld.enroll(fatima);
        anaya.enroll(db);
        System.out.println();
        anaya.showCourses();
        fizza.showCourses();
        ushna.showCourses();
        fatima.showCourses();
        System.out.println();
        db.showStudents();
        oop.showStudents();
        dld.showStudents();
        mvc.showStudents();
    }
}
