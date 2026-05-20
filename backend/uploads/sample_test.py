def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract two numbers"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class Calculator:
    def __init__(self):
        self.result = 0
    
    def calculate(self, operation, a, b):
        if operation == 'add':
            self.result = add(a, b)
        elif operation == 'subtract':
            self.result = subtract(a, b)
        elif operation == 'multiply':
            self.result = multiply(a, b)
        elif operation == 'divide':
            self.result = divide(a, b)
        return self.result
