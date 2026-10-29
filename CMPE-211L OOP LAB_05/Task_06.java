class Profile {
    private String name = "Anaya";
    private String reg = "2026-CYS-S-12";
    private int age = 19;

    public Profile() {
    }
    public Profile(String name) {
        this.name = name;
    }
    public Profile(int age) {
        this.age = age;
    }

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getReg() {
        return reg;
    }
    public void setReg(String reg) {
        this.reg = reg;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
}

public class Task_06 {
    public static void main(String[] args) {
        Profile p1 = new Profile();
        System.out.println(p1.getName() + " and " + p1.getReg());
        Profile p2 = new Profile("sara");
        Profile p3 = new Profile(21);
        System.out.println(p2.getName());
        System.out.println(p3.getAge());
    }
}
