import tkinter as tk
import calendar
from datetime import datetime

class MinimalistCalendar(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the title and basic window configuration
        self.title("Minimalist Calendar")
        self.configure(bg="#333333")
        
        # Set window size to adapt to the screen resolution
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width * 0.6)}x{int(screen_height * 0.7)}")
        self.resizable(True, True)

        # Get the current month and year
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        # Create the calendar display
        self.create_widgets()

    def create_widgets(self):
        # Top navigation bar
        self.nav_frame = tk.Frame(self, bg="#444444")
        self.nav_frame.pack(fill=tk.X, pady=10)

        self.prev_button = tk.Button(self.nav_frame, text="<", command=self.previous_month, bg="#555555", fg="white", bd=0, padx=10, pady=5)
        self.prev_button.pack(side=tk.LEFT, padx=(10, 0))

        self.month_label = tk.Label(self.nav_frame, text="", font=("Helvetica", 16), bg="#444444", fg="white")
        self.month_label.pack(side=tk.LEFT, expand=True)

        self.next_button = tk.Button(self.nav_frame, text=">", command=self.next_month, bg="#555555", fg="white", bd=0, padx=10, pady=5)
        self.next_button.pack(side=tk.RIGHT, padx=(0, 10))

        # Calendar Frame
        self.calendar_frame = tk.Frame(self, bg="#333333")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH)

        # Display the current month and year
        self.update_calendar()

    def update_calendar(self):
        # Clear the calendar frame
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Get the calendar for the current month and year
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        month_name = calendar.month_name[self.current_month]
        self.month_label.config(text=f"{month_name} {self.current_year}")

        # Weekday headers
        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(weekdays):
            lbl = tk.Label(self.calendar_frame, text=day, font=("Helvetica", 12, "bold"), bg="#444444", fg="white", padx=5, pady=5)
            lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Add the days in the calendar
        for row, week in enumerate(cal, 1):
            for col, day in enumerate(week):
                if day != 0:
                    day_label = tk.Label(self.calendar_frame, text=str(day), font=("Helvetica", 12), bg="#555555", fg="white", padx=10, pady=10)
                    day_label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Configure row/column weight for adaptive resizing
        for i in range(len(weekdays)):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.calendar_frame.rowconfigure(i, weight=1)

    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()

if __name__ == "__main__":
    app = MinimalistCalendar()
    app.mainloop()
