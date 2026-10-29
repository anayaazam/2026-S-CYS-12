package Association;

public class Test {
    public static void main(String[] args) {
        Student s = new Student();
        Teacher t1 = new Teacher();
        t1.s1=s;
        t1.display();
    }
}
