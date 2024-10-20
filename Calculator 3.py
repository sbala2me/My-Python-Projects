import tkinter as tk
from tkinter import messagebox
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

def calculate():
    try:
        func = function_var.get()
        x = float(entry_x.get())
        y = None
        if func in ("+", "-", "*", "/", "^"):
            y = float(entry_y.get())

        if func == "+":
            result = add(x, y)
        elif func == "-":
            result = sub(x, y)
        elif func == "*":
            result = mul(x, y)
        elif func == "/":
            result = div(x, y)
        elif func == "^":
            result = pow(x, y)
        elif func == "sqrt":
            result = sqrt(x)
        elif func == "sin":
            result = sin(x)
        elif func == "cos":
            result = cos(x)
        elif func == "tan":
            result = tan(x)
        elif func == "log":
            result = log(x)
        elif func == "exp":
            result = exp(x)
        elif func == "!":
            result = factorial(x)
        else:
            raise ValueError("Invalid function selected!")

        result_label.config(text=f"Result: {result:.4f}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Attam Pota Scientific Calculator")

# Function options
function_var = tk.StringVar(value="+")

# Create widgets
tk.Label(root, text="Select Function:").grid(row=0, column=0, padx=10, pady=10)
functions = ["+", "-", "*", "/", "^", "sqrt", "sin", "cos", "tan", "log", "exp", "!"]
tk.OptionMenu(root, function_var, *functions).grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter X:").grid(row=1, column=0, padx=10, pady=10)
entry_x = tk.Entry(root)
entry_x.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Enter Y (if applicable):").grid(row=2, column=0, padx=10, pady=10)
entry_y = tk.Entry(root)
entry_y.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Calculate", command=calculate).grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Result: ")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()
