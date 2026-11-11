class Book {
    public Book(String name) {
        this.name = name;
    }
    String name;
    Book b;
    public Book(Book b) {
        this.b = b;
    }
    void display(){
        System.out.println(name);
    }
    void abc(){
        System.out.println("anaya");
    }
}
class Library {
    public Library(String name) {
        this.name = name;
    }

    String name;
    Library m;

    public Library(Library m) {
        this.m = m;
    }

    void display() {
        System.out.println(name);
    }
    void cdf(){
        System.out.println("2026-S-CYS-12");
    }
}
public class Task_09{
    public static void main(String[] args){
        Book b1 = new Book("java");
        Library m1 = new Library("b");
        b1.display();
        m1.display();
        b1.abc();
        m1.cdf();


    }
}






