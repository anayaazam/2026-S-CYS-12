// Task_49: [oop]
// mini library system
public class Task_49 {
    static class Book {
        private String title;
        private boolean issued = false;
        Book(String title) { this.title = title; }
        String getTitle() { return title; }
        boolean isIssued() { return issued; }
        void setIssued(boolean issued) { this.issued = issued; }
    }
    static class Member {
        private String name;
        private Book[] borrowed = new Book[3];
        private int count = 0;
        Member(String name) { this.name = name; }
        String getName() { return name; }
        boolean canBorrow() { return count < 3; }
        void addBook(Book b) {
            borrowed[count] = b;
            count++;
        }
        boolean removeBook(Book b) {
            for (int i = 0; i < count; i++) {
                if (borrowed[i] == b) {
                    for (int j = i; j < count - 1; j++) {
                        borrowed[j] = borrowed[j + 1];
                    }
                    borrowed[count - 1] = null;
                    count--;
                    return true;
                }
            }
            return false;
        }
        String holdings() {
            String s = "";
            for (int i = 0; i < count; i++) {
                if (i > 0) s = s + ", ";
                s = s + borrowed[i].getTitle();
            }
            return count == 0 ? "nothing" : s;
        }
    }
    static class Library {
        private Book[] books;
        Library(Book[] books) { this.books = books; }
        void borrow(Member m, Book b) {
            if (b.isIssued()) {
                System.out.println(m.getName() + " cannot borrow '" + b.getTitle() + "': already issued");
            } else if (!m.canBorrow()) {
                System.out.println(m.getName() + " cannot borrow '" + b.getTitle() + "': limit of 3 books reached");
            } else {
                b.setIssued(true);
                m.addBook(b);
                System.out.println(m.getName() + " borrowed '" + b.getTitle() + "'");
            }
            status(m);
        }
        void giveBack(Member m, Book b) {
            if (m.removeBook(b)) {
                b.setIssued(false);
                System.out.println(m.getName() + " returned '" + b.getTitle() + "'");
            } else {
                System.out.println(m.getName() + " does not have '" + b.getTitle() + "'");
            }
            status(m);
        }
        void status(Member m) {
            String available = "";
            for (int i = 0; i < books.length; i++) {
                if (!books[i].isIssued()) {
                    if (!available.isEmpty()) available = available + ", ";
                    available = available + books[i].getTitle();
                }
            }
            System.out.println("   " + m.getName() + " holds: " + m.holdings());
            System.out.println("   Available: " + (available.isEmpty() ? "none" : available));
        }
    }
    public static void main(String[] args) {
        Book b1 = new Book("Java Basics");
        Book b2 = new Book("Data Structures");
        Book b3 = new Book("Algorithms");
        Book b4 = new Book("Databases");
        Library library = new Library(new Book[]{b1, b2, b3, b4});
        Member ali = new Member("Ali");
        Member sara = new Member("Sara");
        library.borrow(ali, b1);
        library.borrow(ali, b2);
        library.borrow(sara, b1);
        library.borrow(ali, b3);
        library.borrow(ali, b4);
        library.giveBack(ali, b1);
        library.borrow(sara, b1);
        library.giveBack(sara, b2);
    }
}
