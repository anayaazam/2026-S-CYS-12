// Task_39: [oop]
// singly linked list from scratch
public class Task_39 {
    static class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static class LinkedList {
        private Node head;
        void insertAtEnd(int value) {
            Node newNode = new Node(value);
            if (head == null) {
                head = newNode;
                return;
            }
            Node current = head;
            while (current.next != null) current = current.next;
            current.next = newNode;
        }
        boolean deleteByValue(int value) {
            if (head == null) return false;
            if (head.value == value) {
                head = head.next;
                return true;
            }
            Node current = head;
            while (current.next != null) {
                if (current.next.value == value) {
                    current.next = current.next.next;
                    return true;
                }
                current = current.next;
            }
            return false;
        }
        void reverse() {
            Node previous = null;
            Node current = head;
            while (current != null) {
                Node next = current.next;
                current.next = previous;
                previous = current;
                current = next;
            }
            head = previous;
        }
        void print() {
            Node current = head;
            while (current != null) {
                System.out.print(current.value);
                if (current.next != null) System.out.print(" -> ");
                current = current.next;
            }
            System.out.println();
        }
    }
    public static void main(String[] args) {
        LinkedList list = new LinkedList();
        for (int v = 10; v <= 50; v += 10) list.insertAtEnd(v);
        System.out.print("List:             ");
        list.print();
        list.deleteByValue(30);
        System.out.print("After deleting 30: ");
        list.print();
        if (!list.deleteByValue(99)) System.out.println("99 is not in the list");
        System.out.print("Before reverse:   ");
        list.print();
        list.reverse();
        System.out.print("After reverse:    ");
        list.print();
    }
}
