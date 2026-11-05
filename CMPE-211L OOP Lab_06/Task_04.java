class engine{
    void start  (){
        System.out.println("The engine has started.");
    }
}
class car{
    void drive(engine e1){
        e1.start();
        System.out.println("The car is  being driven.");
    }
}
public class Task_04 {
    public static void main(String[] args) {
        engine e = new engine();
        car c = new car();
        c.drive(e);
    }
}
