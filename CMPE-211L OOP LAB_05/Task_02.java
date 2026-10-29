import java.util.Scanner;
class Walls {
    private String flavor;
    private int scoops;
    private String coneType;
    private int price;
    public Walls() {
        flavor = "Vanilla";
        scoops = 1;
        coneType = "Sugar";
        calculatePrice();
    }
    public Walls(String flavor, int scoops, String coneType) {
        this.flavor = flavor;
        this.scoops = scoops;
        this.coneType = coneType;
        calculatePrice();
    }
    private void calculatePrice() {
        price = scoops * 75;
        if (coneType.equals("Waffle")) {
            price = price + 40;
        }
    }
    public void display() {
        System.out.println("Flavor: " + flavor);
        System.out.println("Scoops: " + scoops);
        System.out.println("Cone type: " + coneType);
        System.out.println("Price: Rs. " + price);
    }
}
public class Task_02 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("Default order:");
        Walls defaultOrder = new Walls();
        defaultOrder.display();
        System.out.println();
        System.out.println("Flavors:");
        System.out.println("1. Chocolate");
        System.out.println("2. Vanilla");
        System.out.println("3. Strawberry");
        System.out.println("4. Mango");
        System.out.println("5. Tutti Fruit");
        System.out.println("6. Almond Crunch");
        System.out.println("7. Coffee");
        System.out.print("Choose a flavor (1-7): ");
        int flavorChoice = input.nextInt();
        String flavor;
        switch (flavorChoice) {
            case 1:
                flavor = "Chocolate";
                break;
            case 2:
                flavor = "Vanilla";
                break;
            case 3:
                flavor = "Strawberry";
                break;
            case 4:
                flavor = "Mango";
                break;
            case 5:
                flavor = "Tutti Fruit";
                break;
            case 6:
                flavor = "Almond Crunch";
                break;
            case 7:
                flavor = "Coffee";
                break;
            default:
                System.out.println("Invalid choice, Vanilla selected.");
                flavor = "Vanilla";
        }
        System.out.print("Enter number of scoops: ");
        int scoops = input.nextInt();
        System.out.println("Cone types:");
        System.out.println("1. Sugar");
        System.out.println("2. Waffle");
        System.out.print("Choose a cone type (1-2): ");
        int coneChoice = input.nextInt();
        String coneType;
        if (coneChoice == 2) {
            coneType = "Waffle";
        } else {
            coneType = "Sugar";
        }
        System.out.println();
        System.out.println("Your order:");
        Walls order = new Walls(flavor, scoops, coneType);
        order.display();
    }
}
