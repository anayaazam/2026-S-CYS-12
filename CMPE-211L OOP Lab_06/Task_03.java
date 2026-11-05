class Students {
    String name;
    public Students(String name) {
        this.name = name;
    }
}
class Teachers{
    void  students (Students s1){
        System.out.println(s1.name);
    }
}
public class Task_03 {
    public static void main(String[] args) {
        Students s = new Students("anaya");
        Teachers t = new Teachers();
        t.students(s);
    }
}
