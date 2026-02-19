"""
Calculator module with basic arithmetic operations
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base, exponent):
    """Calculate base raised to exponent"""
    return base ** exponent

def square_root(n):
    """Calculate square root of n"""
    if n < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return n ** 0.5

def factorial(n):
    """Calculate factorial of n"""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def is_prime(n):
    """Check if n is a prime number"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    print("Calculator Module Test")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"15 / 3 = {divide(15, 3)}")
    print(f"2^8 = {power(2, 8)}")
    print(f"sqrt(16) = {square_root(16)}")
    print(f"5! = {factorial(5)}")
    print(f"Is 17 prime? {is_prime(17)}")
