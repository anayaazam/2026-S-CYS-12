import java.util.Scanner;

// Task_32: [oop]
// array-based Stack, balanced brackets
public class Task_32 {
    static Scanner sc = new Scanner(System.in);

    static class Stack {
        private char[] data;
        private int top = 0;
        Stack(int size) { data = new char[size]; }
        boolean isEmpty() { return top == 0; }
        void push(char c) {
            if (top == data.length) {
                System.out.println("  Stack overflow: cannot push '" + c + "'");
                return;
            }
            data[top] = c;
            top++;
        }
        char pop() {
            if (isEmpty()) {
                System.out.println("  Stack underflow: nothing to pop");
                return '?';
            }
            top--;
            return data[top];
        }
        char peek() {
            if (isEmpty()) {
                System.out.println("  Stack is empty: nothing to peek");
                return '?';
            }
            return data[top - 1];
        }
    }
    static boolean isBalanced(String text) {
        Stack stack = new Stack(text.length());
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            if (ch == '(' || ch == '{' || ch == '[') {
                stack.push(ch);
            } else if (ch == ')' || ch == '}' || ch == ']') {
                if (stack.isEmpty()) return false;
                char open = stack.pop();
                if (ch == ')' && open != '(') return false;
                if (ch == '}' && open != '{') return false;
                if (ch == ']' && open != '[') return false;
            }
        }
        return stack.isEmpty();
    }
    public static void main(String[] args) {
        System.out.println("Overflow / underflow demo (stack of size 2):");
        Stack small = new Stack(2);
        small.push('a');
        small.push('b');
        small.push('c');
        small.pop();
        small.pop();
        small.pop();
        System.out.print("Enter a string of brackets: ");
        String text = sc.nextLine();
        if (isBalanced(text)) {
            System.out.println("Balanced");
        } else {
            System.out.println("NOT balanced");
        }
    }
}
