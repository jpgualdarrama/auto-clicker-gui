from tkinter import Label, Button, Entry, Radiobutton, StringVar
import threading
import pyautogui
import keyboard  # For global hotkeys

# Intentionally allowing the user to click anywhere on the screen
pyautogui.FAILSAFE = False

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

        self.start_button = Button(master, text="Start (F9)", command=self.start_clicking)
        self.start_button.pack()

        self.stop_button = Button(master, text="Stop (F10)", command=self.stop_clicking)
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
        self.y_label = Label(master, text="Y Position:")
        self.y_label.pack()
        self.y_entry = Entry(master)

        # Set defaults to current mouse position
        mouse_x, mouse_y = pyautogui.position()
        self.x_entry.insert(0, str(mouse_x))
        self.x_entry.pack()
        self.y_entry.insert(0, str(mouse_y))
        self.y_entry.pack()

        # Button to initiate position picking
        self.pick_position_button = Button(master, text="Pick Position (F8)", command=self.enable_position_pick)
        self.pick_position_button.pack()

        self._picking_position = False

        # Run mode selection
        self.run_mode_var = StringVar(value="indefinite")
        self.indefinite_radio = Radiobutton(master, text="Run Indefinitely", variable=self.run_mode_var, value="indefinite", command=self._update_run_mode)
        self.indefinite_radio.pack()
        self.duration_radio = Radiobutton(master, text="Run for Duration", variable=self.run_mode_var, value="duration", command=self._update_run_mode)
        self.duration_radio.pack()
        self.executions_radio = Radiobutton(master, text="Run for Number of Executions", variable=self.run_mode_var, value="executions", command=self._update_run_mode)
        self.executions_radio.pack()

        # Duration input
        self.duration_label = Label(master, text="Duration (seconds):")
        self.duration_label.pack()
        self.duration_entry = Entry(master)
        self.duration_entry.insert(0, "10")
        self.duration_entry.pack()
        self.duration_entry.config(state='disabled')

        # Executions input
        self.executions_label = Label(master, text="Number of Executions:")
        self.executions_label.pack()
        self.executions_entry = Entry(master)
        self.executions_entry.insert(0, "100")
        self.executions_entry.pack()
        self.executions_entry.config(state='disabled')

        self._execution_limit = None

        # Register global hotkeys for start/stop
        self.register_hotkeys()
        # Ensure cleanup on window close
        self.master.protocol("WM_DELETE_WINDOW", self._on_close)

    def register_hotkeys(self):
        """
        Register global hotkeys for start/stop actions. Separated for testability.
        """
        keyboard.add_hotkey('f9', self._on_start_key)
        keyboard.add_hotkey('f10', self._on_stop_key)

    def remove_hotkeys(self):
        """
        Remove global hotkeys for start/stop actions. Separated for testability.
        """
        keyboard.remove_hotkey('f9')
        keyboard.remove_hotkey('f10')

    def _on_start_key(self, event=None):
        """
        Start auto-clicker via F9 keypress.
        """
        self.start_clicking()
        self.label.config(text="Clicking... (Started via F9)")

    def _on_stop_key(self, event=None):
        """
        Stop auto-clicker via F10 keypress.
        """
        self.stop_clicking()
        self.label.config(text="Stopped (via F10)")

    def _on_close(self):
        """
        Remove global hotkeys and close window.
        """
        self.remove_hotkeys()
        self.master.destroy()

    def enable_position_pick(self):
        """
        Enable position picking mode. Next F8 press will set position.
        """
        if not self._picking_position:
            self._picking_position = True
            self.label.config(text="Move mouse to desired position and press F8")
            self.master.bind('<F8>', self.set_position_from_mouse)

    def set_position_from_mouse(self, event=None):
        """
        Set X and Y entry fields to current mouse position when F8 is pressed, only if picking mode is enabled.
        """
        if self._picking_position:
            x, y = pyautogui.position()
            self.x_entry.delete(0, 'end')
            self.x_entry.insert(0, str(x))
            self.y_entry.delete(0, 'end')
            self.y_entry.insert(0, str(y))
            self.label.config(text=f"Position set to ({x}, {y}) via F8")
            self._picking_position = False
            self.master.unbind('<F8>')

    def _update_run_mode(self):
        """
        Enable/disable duration field based on selected run mode.
        """
        mode = self.run_mode_var.get()
        if mode == "duration":
            self.duration_entry.config(state='normal')
            self.executions_entry.config(state='disabled')
        elif mode == "executions":
            self.duration_entry.config(state='disabled')
            self.executions_entry.config(state='normal')
        else:
            self.duration_entry.config(state='disabled')
            self.executions_entry.config(state='disabled')

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

    def parse_duration(self, value):
        """
        Parse the duration value from string input. Returns a positive integer.
        Raises ValueError if invalid.
        """
        duration = int(value)
        if duration > 0:
            return duration
        raise ValueError("Duration must be a positive integer.")

    def parse_executions(self, value):
        """
        Parse the executions value from string input. Returns a positive integer.
        Raises ValueError if invalid.
        """
        executions = int(value)
        if executions > 0:
            return executions
        raise ValueError("Executions must be a positive integer.")

    def _update_timer(self):
        """
        Update countdown timer every second. Stop clicking when time is up.
        """
        if self._timer_running and self.is_clicking:
            self._remaining_time -= 1
            self.label.config(text=f"Clicking... ({self._remaining_time}s left)")
            if self._remaining_time <= 0:
                self.stop_clicking()
                self.label.config(text="Time is up. Stopped.")
            else:
                self.master.after(1000, self._update_timer)

    def start_clicking(self):
        """
        Event handler for the Start button. Sets clicking state to True and updates label.
        Only starts clicking if interval and position are valid. Uses duration only if selected.
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
            run_mode = self.run_mode_var.get()
            if run_mode == "duration":
                try:
                    duration = self.parse_duration(self.duration_entry.get())
                except ValueError:
                    self.label.config(text="Invalid duration. Please enter a positive integer.")
                    return
                self._timer_running = True
                self._remaining_time = duration
                self._execution_limit = None
            elif run_mode == "executions":
                try:
                    executions = self.parse_executions(self.executions_entry.get())
                except ValueError:
                    self.label.config(text="Invalid executions. Please enter a positive integer.")
                    return
                self._timer_running = False
                self._remaining_time = 0
                self._execution_limit = executions
            else:
                self._timer_running = False
                self._remaining_time = 0
                self._execution_limit = None

            self.is_clicking = True
            self.label.config(text="Clicking...")
            self.interval = interval
            self.position = position
            self._executions_done = 0
            self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
            self.click_thread.start()

            if run_mode == "duration":
                self.master.after(1000, self._update_timer)

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
            if self._execution_limit is not None:
                self._executions_done += 1
                remaining = self._execution_limit - self._executions_done
                if remaining > 0:
                    self.label.config(text=f"Clicking... {remaining} executions left")
                if self._executions_done >= self._execution_limit:
                    self.stop_clicking()
                    self.label.config(text=f"Completed {self._execution_limit} executions.")