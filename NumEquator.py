import tkinter as tk
from tkinter import messagebox
from sympy import isprime


# Helper functions
def generate_equations():
    try:
        target = int(entry_number.get())
        operation = operation_var.get()
        number_type = number_type_var.get()

        if target <= 0:
            raise ValueError("The number must be greater than zero.")

        # Generate the appropriate numbers based on the type
        numbers = range(1, target + 1)
        if number_type == "Prime":
            numbers = [num for num in numbers if isprime(num)]
        elif number_type == "Composite":
            numbers = [num for num in numbers if num > 1 and not isprime(num)]

        equations = []
        for x in numbers:
            for y in numbers:
                if operation == "Addition" and x + y == target:
                    equations.append(f"{x} + {y} = {target}")
                elif operation == "Subtraction" and x - y == target:
                    equations.append(f"{x} - {y} = {target}")
                elif operation == "Multiplication" and x * y == target:
                    equations.append(f"{x} x {y} = {target}")
                elif operation == "Division" and y != 0 and x / y == target:
                    equations.append(f"{x} ÷ {y} = {target}")

        if not equations:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "No equations found for the given input.")
        else:
            display_equations(equations)
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def display_equations(equations):
    result_text.delete("1.0", tk.END)
    for eq in equations:
        result_text.insert(tk.END, eq + "\n")


# GUI setup
root = tk.Tk()
root.title("Equation Generator")
root.geometry("700x500")
root.configure(bg="black")

# Aesthetic styles
font_label = ("Helvetica", 12, "bold")
font_button = ("Helvetica", 12, "bold")
font_result = ("Courier", 10)
fg_color = "white"
bg_color = "black"
btn_color = "#1e90ff"

# Number input
frame_number = tk.Frame(root, bg=bg_color)
frame_number.pack(pady=10)
tk.Label(frame_number, text="Enter a Number:", font=font_label, fg=fg_color, bg=bg_color).grid(row=0, column=0, padx=5)
entry_number = tk.Entry(frame_number, font=font_label, bg="gray", fg="white", insertbackground="white")
entry_number.grid(row=0, column=1, padx=5)

# Number type selection
frame_type = tk.Frame(root, bg=bg_color)
frame_type.pack(pady=10)
tk.Label(frame_type, text="Number Type:", font=font_label, fg=fg_color, bg=bg_color).grid(row=0, column=0, padx=5)
number_type_var = tk.StringVar(value="All")
tk.Radiobutton(frame_type, text="All", variable=number_type_var, value="All", font=font_label, fg=fg_color, bg=bg_color, selectcolor=bg_color).grid(row=0, column=1)
tk.Radiobutton(frame_type, text="Prime", variable=number_type_var, value="Prime", font=font_label, fg=fg_color, bg=bg_color, selectcolor=bg_color).grid(row=0, column=2)
tk.Radiobutton(frame_type, text="Composite", variable=number_type_var, value="Composite", font=font_label, fg=fg_color, bg=bg_color, selectcolor=bg_color).grid(row=0, column=3)

# Operation selection
frame_operation = tk.Frame(root, bg=bg_color)
frame_operation.pack(pady=10)
tk.Label(frame_operation, text="Operation:", font=font_label, fg=fg_color, bg=bg_color).grid(row=0, column=0, padx=5)
operation_var = tk.StringVar(value="Addition")
tk.OptionMenu(frame_operation, operation_var, "Addition", "Subtraction", "Multiplication", "Division").config(
    font=font_label, bg="gray", fg="white", activebackground=btn_color
)
operation_menu = tk.OptionMenu(frame_operation, operation_var, "Addition", "Subtraction", "Multiplication", "Division")
operation_menu.config(font=font_label, bg="gray", fg="white", activebackground=btn_color)
operation_menu.grid(row=0, column=1)

# Generate button
btn_generate = tk.Button(root, text="Generate Equations", font=font_button, bg=btn_color, fg="white", command=generate_equations)
btn_generate.pack(pady=10)

# Results display
result_text = tk.Text(root, wrap="word", height=15, width=70, font=font_result, bg="gray", fg="white", insertbackground="white")
result_text.pack(pady=10)

# Run the application
root.mainloop()
