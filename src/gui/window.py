
from tkinter import Label, Button, Entry
import threading
import pyautogui

class Window:
    """
    Main application window for the Auto Clicker GUI tool.
    Manages GUI widgets, event handlers, and clicker state.
    """
    def __init__(self, master):
        """
        Initialize the main window, widgets, and state variables.
        :param master: Tkinter root window
        """
        self.master = master
        master.title("Auto Clicker")

        self.label = Label(master, text="Auto Clicker Tool")
        self.label.pack()

        self.start_button = Button(master, text="Start", command=self.start_clicking)
        self.start_button.pack()

        self.stop_button = Button(master, text="Stop", command=self.stop_clicking)
        self.stop_button.pack()

        self.is_clicking = False
        self.click_thread = None

        # Interval input
        self.interval_label = Label(master, text="Click Interval (seconds):")
        self.interval_label.pack()
        self.interval_entry = Entry(master)
        self.interval_entry.insert(0, "0.1")
        self.interval_entry.pack()

        # X and Y position inputs
        self.x_label = Label(master, text="X Position:")
        self.x_label.pack()
        self.x_entry = Entry(master)
        self.x_entry.insert(0, "0")
        self.x_entry.pack()

        self.y_label = Label(master, text="Y Position:")
        self.y_label.pack()
        self.y_entry = Entry(master)
        self.y_entry.insert(0, "0")
        self.y_entry.pack()

    def parse_interval(self, value):
        """
        Parse the interval value from string input. Returns a positive float.
        Raises ValueError if invalid.
        """
        # float() will raise ValueError if conversion fails
        interval = float(value)
        if interval > 0:
            return interval
        raise ValueError("Interval must be a positive number.")

    def parse_position(self):
        """
        Parse x and y position from input boxes. Returns tuple (x, y) as integers, clamped to screen bounds.
        Raises ValueError if invalid.
        """

        # int() will raise ValueError if conversion fails
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())
        screen_width, screen_height = pyautogui.size()
        x = max(0, min(x, screen_width - 1))
        y = max(0, min(y, screen_height - 1))
        return x, y

    def start_clicking(self):
        """
        Event handler for the Start button. Sets clicking state to True and updates label.
        Only starts clicking if interval and position are valid.
        """
        if not self.is_clicking:
            try:
                interval = self.parse_interval(self.interval_entry.get())
            except ValueError:
                self.label.config(text="Invalid interval. Please enter a positive number.")
                return
            try:
                position = self.parse_position()
            except ValueError:
                self.label.config(text="Invalid position. Please enter valid X and Y coordinates.")
                return
            self.is_clicking = True
            self.label.config(text="Clicking...")
            self.interval = interval
            self.position = position
            self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
            self.click_thread.start()

    def stop_clicking(self):
        """
        Event handler for the Stop button. Sets clicking state to False and updates label.
        """
        self.is_clicking = False
        self.label.config(text="Stopped")

    def _click_loop(self):
        """
        Internal loop that performs mouse clicks while is_clicking is True.
        Designed for testability and clarity.
        """
        while self.is_clicking:
            pyautogui.click(*self.position)
            pyautogui.sleep(self.interval)