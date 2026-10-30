// Task_29: [oop]
// Employee and Manager (overrides calculateSalary, uses super)
public class Task_29 {
    static class Employee {
        protected String name;
        protected double baseSalary;
        Employee(String name, double baseSalary) {
            this.name = name;
            this.baseSalary = baseSalary;
        }

        double calculateSalary() { return baseSalary; }
        String getName() { return name; }
    }
    static class Manager extends Employee {
        private double bonus;
        Manager(String name, double baseSalary, double bonus) {
            super(name, baseSalary);
            this.bonus = bonus;
        }
        double calculateSalary() {
            return super.calculateSalary() + bonus;
        }
    }
    public static void main(String[] args) {
        Employee[] staff = new Employee[3];
        staff[0] = new Employee("Ali", 3000);
        staff[1] = new Manager("Sara", 5000, 1500);
        staff[2] = new Employee("Omar", 3500);
        for (int i = 0; i < staff.length; i++) {
            System.out.println(staff[i].getName() + " earns " + staff[i].calculateSalary());
        }
    }
}
