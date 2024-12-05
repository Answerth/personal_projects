import tkinter as tk
from tkinter import simpledialog, Menu
from tkinter import font as tkfont

class CountdownApp:
    def __init__(self, root, countdown_time=10, alert_color="#FF0000", default_bg="black"):
        self.root = root
        self.countdown_time = countdown_time
        self.time_left = countdown_time
        self.alert_color = alert_color
        self.default_bg = default_bg
        self.countdown_active = False
        self.always_on_top = False
        self.auto_continue = True  # Toggle behavior for reset and continue
        self.timer_id = None  # To keep track of the after() call

        # Initialize font settings
        self.font_name = "Arial"
        self.font_size = 60
        self.label_font = tkfont.Font(family=self.font_name, size=self.font_size)

        # Configure the window
        self.root.title("Countdown Timer")
        self.root.geometry("400x400")  # Default size, but resizable
        self.root.configure(bg=self.default_bg)
        self.root.bind("<Button-1>", self.start_or_reset_timer)
        self.root.bind("<Configure>", self.on_resize)  # Bind resize event

        # Create a menu to toggle settings
        self.create_menu()

        # Create and configure the label to display the countdown
        self.label = tk.Label(self.root, text=self.format_time(self.time_left), font=self.label_font, fg="white", bg=self.default_bg)
        self.label.pack(expand=True)

    def format_time(self, seconds):
        """Format seconds into a MM:SS format."""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def start_or_reset_timer(self, event=None):
        """Start or reset the countdown based on the current state."""
        self.root.configure(bg=self.default_bg)

        # Cancel any existing after() calls to prevent multiple timers
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.time_left = self.countdown_time  # Reset timer to initial countdown time
        self.label.config(text=self.format_time(self.time_left))

        if self.auto_continue or not self.countdown_active:
            self.countdown_active = True
            self.update_timer()
        else:
            self.countdown_active = False

    def update_timer(self):
        """Update the countdown timer every second."""
        if self.time_left > 0 and self.countdown_active:
            self.time_left -= 1
            self.label.config(text=self.format_time(self.time_left))
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.trigger_alert()

    def trigger_alert(self):
        """Change the background to red and reset the timer state."""
        self.root.configure(bg=self.alert_color)
        self.label.config(text="00:00")
        self.countdown_active = False

        # Cancel any pending after() calls
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def create_menu(self):
        """Create a menu bar with options to toggle settings."""
        menubar = Menu(self.root)

        # Settings Menu
        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Toggle Always on Top", command=self.toggle_always_on_top)
        settings_menu.add_command(label="Change Countdown Time", command=self.change_countdown_time)
        settings_menu.add_command(label="Toggle Auto Continue", command=self.toggle_auto_continue)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.root.config(menu=menubar)

    def toggle_always_on_top(self):
        """Toggle the 'Always on Top' feature for the window."""
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)

    def change_countdown_time(self):
        """Prompt the user to enter a new countdown time."""
        new_time = simpledialog.askinteger("Input", "Enter new countdown time in seconds:", minvalue=1, maxvalue=3600)
        if new_time:
            self.countdown_time = new_time
            self.time_left = new_time
            self.label.config(text=self.format_time(self.time_left))

    def toggle_auto_continue(self):
        """Toggle the auto-continue feature for resetting the countdown."""
        self.auto_continue = not self.auto_continue
        if self.auto_continue:
            print("Auto Continue: Enabled")
        else:
            print("Auto Continue: Disabled")

    def on_resize(self, event):
        """Adjust the font size when the window is resized."""
        # Calculate the new font size based on the window's dimensions
        new_width = event.width
        new_height = event.height

        # Adjust font size relative to window size
        new_font_size = min(int(new_height / 3), int(new_width / 6))
        if new_font_size < 10:
            new_font_size = 10  # Set a minimum font size

        # Update the font size
        self.label_font.configure(size=new_font_size)

if __name__ == "__main__":
    root = tk.Tk()

    # Get user input for countdown time (in seconds)
    user_input = simpledialog.askinteger("Input", "Enter countdown time in seconds:", minvalue=1, maxvalue=3600)
    countdown_time = user_input if user_input else 10  # Default 10 seconds if no input

    app = CountdownApp(root, countdown_time=countdown_time)
    root.mainloop()
