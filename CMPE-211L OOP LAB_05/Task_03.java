import java.util.Scanner;
class Product {
    private String name;
    private int price;
    private int quantity;
    private static int totalProduct = 0;
    private static Scanner input = new Scanner(System.in);
    public Product() {
        name = "Unknown";
        price = 0;
        quantity = 0;
        counter();
    }
    public Product(String name, int price, int quantity) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
        counter();
    }
    public void getData() {
        System.out.print("Enter product name: ");
        name = input.next();
        System.out.print("Enter product price: ");
        price = input.nextInt();
        System.out.print("Enter product quantity: ");
        quantity = input.nextInt();
    }
    public void display() {
        System.out.println("Name: " + name + ", Price: " + price + ", Quantity: " + quantity);
    }
    public static void counter() {
        totalProduct++;
    }
    public static int countProduct() {
        return totalProduct;
    }
}
public class Task_03 {
    public static void main(String[] args) {
        Product p1 = new Product("Pen", 20, 100);
        Product p2 = new Product("Notebook", 150, 50);
        Product p3 = new Product("Marker", 60, 30);
        Product p4 = new Product();
        Product p5 = new Product();
        System.out.println("Enter data for product 4:");
        p4.getData();
        System.out.println();
        p1.display();
        p2.display();
        p3.display();
        p4.display();
        p5.display();
        System.out.println();
        System.out.println("Total products: " + Product.countProduct());
    }
}
