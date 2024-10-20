import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class ModernCalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Calendar App")
        self.geometry("450x400")
        self.configure(bg="#2e2e2e")

        # Header with current month and year
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        self.header_frame = tk.Frame(self, bg="#2e2e2e")
        self.header_frame.pack(pady=10)

        self.month_label = tk.Label(self.header_frame, text="", font=("Helvetica", 18, "bold"), fg="white", bg="#2e2e2e")
        self.month_label.pack(side="left", padx=20)

        prev_button = ttk.Button(self.header_frame, text="<", command=self.prev_month)
        prev_button.pack(side="left", padx=10)

        next_button = ttk.Button(self.header_frame, text=">", command=self.next_month)
        next_button.pack(side="left", padx=10)

        # Create frame for calendar grid
        self.calendar_frame = tk.Frame(self, bg="#2e2e2e")
        self.calendar_frame.pack()

        self.create_calendar(self.current_year, self.current_month)

    def create_calendar(self, year, month):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Display month and year
        self.month_label.config(text=f"{calendar.month_name[month]} {year}")

        # Add day labels
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Helvetica", 12, "bold"), 
                     bg="#3e3e3e", fg="white", width=5).grid(row=0, column=i, padx=1, pady=1)

        # Get the calendar for the given month and year
        cal = calendar.monthcalendar(year, month)

        # Display the dates
        for row_num, week in enumerate(cal, start=1):
            for col_num, day in enumerate(week):
                if day == 0:
                    day_label = tk.Label(self.calendar_frame, text="", font=("Helvetica", 12), 
                                         bg="#2e2e2e", width=5, height=2)
                else:
                    day_label = tk.Label(self.calendar_frame, text=day, font=("Helvetica", 12), 
                                         bg="#1e90ff", fg="white", width=5, height=2)
                day_label.grid(row=row_num, column=col_num, padx=1, pady=1)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.create_calendar(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.create_calendar(self.current_year, self.current_month)

if __name__ == "__main__":
    app = ModernCalendarApp()
    app.mainloop()
