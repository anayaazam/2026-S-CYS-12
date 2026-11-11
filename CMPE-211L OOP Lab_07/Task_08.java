class Department {
    String name;
    public Department(String name) {
        this.name = name;
    }
    Department d;
    public Department(Department d) {
        this.d = d;
    }
    void display(){
        System.out.println(name);
    }
}

class Teacher {
    String name;
    public Teacher(String name) {
        this.name = name;
    }
    Teacher t;
    public Teacher(Teacher t) {
        this.t = t;
    }
    void display(){
        System.out.println(name);
    }
}
public class Task_08 {
    public static void main(String[] args){
        Teacher t1 = new Task_04.Teacher("sir");
        Department d1 = new Task_04.Department("cys");
        t1.display();
        d1.display();
    }
}

