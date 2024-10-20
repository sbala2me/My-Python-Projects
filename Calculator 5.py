import tkinter as tk

class MinimalistCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the title and basic window configuration
        self.title("Minimalist Calculator")
        self.configure(bg="#333333")

        # Set window size to adapt to screen resolution
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width * 0.3)}x{int(screen_height * 0.5)}")
        self.resizable(True, True)

        # Display and button setup
        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        # Display for the calculator
        self.display = tk.Entry(self, font=("Helvetica", 24), borderwidth=0, relief="flat", bg="#222222", fg="white", justify="right")
        self.display.pack(expand=True, fill="both", padx=10, pady=10)

        # Create a frame for the buttons
        button_frame = tk.Frame(self, bg="#333333")
        button_frame.pack(expand=True, fill="both")

        # Button layout
        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('0', '.', '=', '+')
        ]

        # Add buttons to the frame
        for row_index, row in enumerate(buttons):
            for col_index, button_text in enumerate(row):
                button = tk.Button(button_frame, text=button_text, font=("Helvetica", 18), bg="#555555", fg="white",
                                   bd=0, padx=10, pady=10, command=lambda txt=button_text: self.on_button_click(txt))
                button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)

        # Configure row/column weight for adaptive resizing
        for i in range(len(buttons)):
            button_frame.rowconfigure(i, weight=1)
            button_frame.columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "=":
            try:
                # Evaluate the expression and display the result
                result = str(eval(self.expression))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                self.expression = result
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.expression = ""
        elif char in "0123456789.+-*/":
            # Add to the expression
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
        else:
            # Clear on 'C' press or invalid input
            self.display.delete(0, tk.END)
            self.expression = ""

if __name__ == "__main__":
    app = MinimalistCalculator()
    app.mainloop()
