class details {
    String name;
    int age;
    private String cnic;

    public String getCnic() {
        return cnic;
    }

    public void setCnic(String cnic) {
        this.cnic = cnic;
    }
}

public class Task_03 {
    public static void main(String[] args) {
        details n = new details();
        n.setCnic("0123456789");
        n.name = "Anaya";
        n.age = 19;
        System.out.println(n.name);
        System.out.println(n.age);
        System.out.println(n.getCnic());
    }
}
