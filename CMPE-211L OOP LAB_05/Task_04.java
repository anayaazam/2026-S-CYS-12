class student {
    private String name;
    private int age;

    public student(String name) {
        this.name = name;
    }
    public student(int age) {
        this.age = age;
    }

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
}

public class Task_04 {
    public static void main(String[] args) {
        student s1 = new student("Anaya");
        student s2 = new student(19);
        System.out.println(s1.getName());
        System.out.println(s2.getAge());
        s1.setAge(20);
        System.out.println(s1.getAge());
    }
}
