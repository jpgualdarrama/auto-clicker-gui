
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

    def parse_interval(self, value):
        """
        Parse the interval value from string input. Returns a positive float or default 0.1.
        """
        try:
            interval = float(value)
            if interval > 0:
                return interval
        except ValueError:
            pass
        return 0.1

    def start_clicking(self):
        """
        Event handler for the Start button. Sets clicking state to True and updates label.
        """
        if not self.is_clicking:
            self.is_clicking = True
            self.label.config(text="Clicking...")
            self.interval = self.parse_interval(self.interval_entry.get())
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
            pyautogui.click()
            pyautogui.sleep(self.interval)