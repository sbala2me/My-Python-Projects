import tkinter as tk
from tkinter import messagebox

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "ey thumbi poda attam pota pakka pushpa adadey."

def perform_calculation():
    try:
        operation = operation_var.get()
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())

        if operation == "Add":
            result = add(num1, num2)
        elif operation == "Subtract":
            result = subtract(num1, num2)
        elif operation == "Multiply":
            result = multiply(num1, num2)
        elif operation == "Divide":
            result = divide(num1, num2)
        else:
            raise ValueError("Invalid operation")

        result_label.config(text=f"Result: {result}")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Create the main window
root = tk.Tk()
root.title("Attam Pota Simple Calculator")

# Create widgets
operation_var = tk.StringVar(value="Add")

tk.Label(root, text="Select Operation:").grid(row=0, column=0, padx=10, pady=10)
operations = ["Add", "Subtract", "Multiply", "Divide"]
tk.OptionMenu(root, operation_var, *operations).grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter First Number:").grid(row=1, column=0, padx=10, pady=10)
entry_num1 = tk.Entry(root)
entry_num1.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Enter Second Number:").grid(row=2, column=0, padx=10, pady=10)
entry_num2 = tk.Entry(root)
entry_num2.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Calculate", command=perform_calculation).grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Result: ")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()
