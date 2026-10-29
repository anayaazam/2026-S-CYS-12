package Cars;

public class Test {
    public static void main(String[] args) {
        Brand b1 = new Brand();
        Car car = new Car();
        b1.c = car;
        b1.display();
    }
}
