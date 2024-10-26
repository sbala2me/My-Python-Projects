import tkinter as tk
import webbrowser

# Function to open the URL
def open_url():
    webbrowser.open("https://y8tireu.github.io/Website2/")

# Create the main window
root = tk.Tk()
root.title("Website")

# Set the window background color to black
root.configure(bg='black')

# Create a green button with customized color
button = tk.Button(root, text="Open Website", command=open_url,
                   bg='green', fg='white', font=('Arial', 14, 'bold'))

# Place the button and adjust padding
button.pack(pady=20)

# Run the application
root.mainloop()
