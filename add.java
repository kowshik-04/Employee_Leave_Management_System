public class add {
    
    /**
     * Adds two integers and returns the result
     * @param a First integer
     * @param b Second integer
     * @return Sum of a and b
     */
    public int addTwoNumbers(int a, int b) {
        return a + b;
    }
    
    /**
     * Adds three integers and returns the result
     * @param a First integer
     * @param b Second integer
     * @param c Third integer
     * @return Sum of a, b, and c
     */
    public int addThreeNumbers(int a, int b, int c) {
        return a + b + c;
    }
    
    /**
     * Adds an array of integers and returns the sum
     * @param numbers Array of integers to add
     * @return Sum of all numbers in the array
     */
    public int addArray(int[] numbers) {
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        return sum;
    }
    
    /**
     * Adds two double values and returns the result
     * @param a First double
     * @param b Second double
     * @return Sum of a and b
     */
    public double addDoubles(double a, double b) {
        return a + b;
    }
    
    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        add calculator = new add();
        
        System.out.println("2 + 3 = " + calculator.addTwoNumbers(2, 3));
        System.out.println("1 + 2 + 3 = " + calculator.addThreeNumbers(1, 2, 3));
        System.out.println("Sum of [1,2,3,4,5] = " + calculator.addArray(new int[]{1, 2, 3, 4, 5}));
        System.out.println("2.5 + 3.7 = " + calculator.addDoubles(2.5, 3.7));
    }
}
