import tkinter as tk
from tkinter import scrolledtext

def start_loop():
    global running, count, max_repetitions
    try:
        max_repetitions = int(repetitions_entry.get())  # Get the desired repetitions from the entry field
    except ValueError:
        max_repetitions = 100000  # Set default value if the input is invalid
    count = 0
    running = True
    update_text()

def stop_loop():
    global running
    running = False

def update_text():
    global count
    if running and count < max_repetitions:  # Use the user-defined repetitions limit
        text_area.insert(tk.END, "Amuku Damkuka Amkuku Dumal Attam pota Attam Pota Pakka Pushpa Addadey pushpa enna thotu ey thumbi poda attam pota pakka pushpa adadey")
        text_area.see(tk.END)  # Auto-scroll to the end
        count += 1
        root.after(10, update_text)  # Adjust the delay if needed (in milliseconds)

# Initialize the main window
root = tk.Tk()
root.title("Amuku Dumal Loop")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size relative to screen size (e.g., 80% of screen width and height)
window_width = int(screen_width * 0.5)  # Adjust this percentage as needed
window_height = int(screen_height * 0.5)
root.geometry(f"{window_width}x{window_height}")

# Create a text area to display the output
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

# Create an entry to input the number of repetitions
repetitions_label = tk.Label(root, text="Enter number of repetitions:")
repetitions_label.pack(padx=10, pady=5)

repetitions_entry = tk.Entry(root, width=10)
repetitions_entry.pack(padx=10, pady=5)
repetitions_entry.insert(0, "100000")  # Default value for repetitions

# Create start and stop buttons
button_frame = tk.Frame(root)  # Create a frame for buttons
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start", command=start_loop)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_loop)
stop_button.pack(side=tk.LEFT, padx=10)

# Initialize loop control variable
running = False
count = 0
max_repetitions = 100000  # Default repetitions

# Run the Tkinter event loop
root.mainloop()
