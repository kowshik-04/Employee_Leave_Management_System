public class Division {
    int a;
    int b;

    // Constructor
    public Division(int a, int b) {
        this.a = a;
        this.b = b;
    }

    // Method to perform division
    public double divide() {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return (double) a / b;
    }

    // Main method to test
    public static void main(String[] args) {
        Division d = new Division(10, 2);
        System.out.println("Result: " + d.divide());
    }
}