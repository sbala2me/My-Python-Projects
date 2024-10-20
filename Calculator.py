import math

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def div(x, y):
    if y == 0:
        raise ValueError("You made An Amuku Damku Amuku Dumal Mistake")
    return x / y

def pow(x, y):
    return x ** y

def sqrt(x):
    return math.sqrt(x)

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def log(x):
    return math.log(x)

def exp(x):
    return math.exp(x)

def factorial(x):
    if x < 0:
        raise ValueError("Factorial is not defined for negative numbers!")
    result = 1
    for i in range(1, int(x) + 1):
        result *= i
    return result

def main():
    print("Welcome to the Attam Pota Scientific Calculator!")
    print("Available functions:")
    print("  +: addition")
    print("  -: subtraction")
    print("  *: multiplication")
    print("  /: division")
    print("  ^: exponentiation")
    print("  sqrt: square root")
    print("  sin: sine")
    print("  cos: cosine")
    print("  tan: tangent")
    print("  log: natural logarithm")
    print("  exp: exponential function")
    print("  !: factorial")
    print("  quit: exit the calculator")

    while True:
        user_input = input("Enter a function and arguments (e.g. '+ 2 3'): ")
        if user_input.lower() == "quit":
            break
        try:
            func, *args = user_input.split()
            args = [float(arg) for arg in args]
            if func == "+":
                result = add(args[0], args[1])
            elif func == "-":
                result = sub(args[0], args[1])
            elif func == "*":
                result = mul(args[0], args[1])
            elif func == "/":
                result = div(args[0], args[1])
            elif func == "^":
                result = pow(args[0], args[1])
            elif func == "sqrt":
                result = sqrt(args[0])
            elif func == "sin":
                result = sin(args[0])
            elif func == "cos":
                result = cos(args[0])
            elif func == "tan":
                result = tan(args[0])
            elif func == "log":
                result = log(args[0])
            elif func == "exp":
                result = exp(args[0])
            elif func == "!":
                result = factorial(args[0])
            else:
                print("Invalid function!")
                continue
            print(f"Result: {result:.4f}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
