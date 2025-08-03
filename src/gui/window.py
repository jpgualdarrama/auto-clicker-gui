from tkinter import Label, Button, Entry, Radiobutton, StringVar, ttk
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

        # Set defaults to current mouse position
        mouse_x, mouse_y = pyautogui.position()


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

        # --- Action List Table and Controls ---
        self.actions = []  # List of dicts: {x, y, interval, type}
        default_action = {
            "x": mouse_x,
            "y": mouse_y,
            "interval": 0.1,
            "type": "click"
        }
        self.actions.append(default_action)
        self.action_table = ttk.Treeview(self.master, columns=("x", "y", "interval", "type"), show="headings", selectmode="browse", height=6)
        for col in ("x", "y", "interval", "type"):
            self.action_table.heading(col, text=col.capitalize())
            self.action_table.column(col, width=80, anchor="center")
        self.action_table.pack(pady=8)

        # Table controls
        self.action_controls_frame = ttk.Frame(self.master)
        self.action_controls_frame.pack()

        self.add_action_btn = Button(self.action_controls_frame, text="Add", command=self._add_action)
        self.add_action_btn.grid(row=0, column=0, padx=2)
        self.remove_action_btn = Button(self.action_controls_frame, text="Remove", command=self._remove_action)
        self.remove_action_btn.grid(row=0, column=1, padx=2)
        self.move_up_btn = Button(self.action_controls_frame, text="Move Up", command=self._move_action_up)
        self.move_up_btn.grid(row=0, column=2, padx=2)
        self.move_down_btn = Button(self.action_controls_frame, text="Move Down", command=self._move_action_down)
        self.move_down_btn.grid(row=0, column=3, padx=2)
        # Pick Position button, initially disabled
        self.pick_position_button = Button(self.action_controls_frame, text="Pick Position (F8)", command=self.enable_position_pick, state="disabled")
        self.pick_position_button.grid(row=0, column=4, padx=2)

        # Removed new action input boxes; users add/edit actions directly in the table

        # Bind double-click for editing
        self.action_table.bind("<Double-1>", self._edit_action_cell)
        # Enable Pick Position only when a row is selected
        self.action_table.bind("<<TreeviewSelect>>", self._on_table_select)

        # Show default action in table on load
        self._refresh_action_table()

    def _on_table_select(self, event=None):
        """Enable Pick Position button only if a row is selected."""
        sel = self.action_table.selection()
        if sel:
            self.pick_position_button.config(state="normal")
        else:
            self.pick_position_button.config(state="disabled")

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
        Enable position picking mode. Next F8 press will set X/Y of selected action in table.
        """
        if not self._picking_position:
            self._picking_position = True
            self.label.config(text="Move mouse to desired position and press F8 (updates selected action)")
            self.master.bind('<F8>', self.set_position_from_mouse)

    def set_position_from_mouse(self, event=None):
        """
        Set X and Y of selected action in table to current mouse position when F8 is pressed, only if picking mode is enabled.
        """
        if self._picking_position:
            x, y = pyautogui.position()
            sel = self.action_table.selection()
            if sel:
                idx = int(sel[0])
                if 0 <= idx < len(self.actions):
                    self.actions[idx]["x"] = x
                    self.actions[idx]["y"] = y
                    self._refresh_action_table()
                    self.action_table.selection_set(str(idx))
            # if nothing is selected, do nothing

            self._picking_position = False
            self.master.unbind('<F8>')
            self.label.config(text="Auto Clicker Tool")

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

    def _add_action(self):
        """Add a new blank action to the table and internal list."""
        action = {"x": 0, "y": 0, "interval": 0.1, "type": "click"}
        self.actions.append(action)
        self._refresh_action_table()

    def _remove_action(self):
        """Remove the currently selected action from the table and list."""
        sel = self.action_table.selection()
        if sel:
            idx = int(sel[0])
            if 0 <= idx < len(self.actions):
                del self.actions[idx]
                self._refresh_action_table()

    def _edit_action_cell(self, event):
        """Enable editing of a cell in the table by double-click."""
        region = self.action_table.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.action_table.identify_row(event.y)
        col = self.action_table.identify_column(event.x)
        if not row_id or not col:
            return
        idx = int(row_id)
        col_idx = int(col.replace("#", "")) - 1
        col_name = ("x", "y", "interval", "type")[col_idx]
        x0, y0, width, height = self.action_table.bbox(row_id, col)
        edit_win = Entry(self.action_table, width=8)
        edit_win.place(x=x0, y=y0, width=width, height=height)
        edit_win.insert(0, str(self.actions[idx][col_name]))
        edit_win.focus()
        def save_edit(event=None):
            val = edit_win.get()
            try:
                if col_name in ("x", "y"):
                    val = int(val)
                elif col_name == "interval":
                    val = float(val)
            except Exception:
                edit_win.destroy()
                return
            self.actions[idx][col_name] = val
            edit_win.destroy()
            self._refresh_action_table()
        edit_win.bind("<Return>", save_edit)
        edit_win.bind("<FocusOut>", lambda e: edit_win.destroy())

    def _refresh_action_table(self):
        """Refresh the table to show current actions."""
        self.action_table.delete(*self.action_table.get_children())
        for i, action in enumerate(self.actions):
            self.action_table.insert("", "end", iid=str(i), values=(action["x"], action["y"], action["interval"], action["type"]))

    def _move_action_up(self):
        sel = self.action_table.selection()
        if sel:
            idx = int(sel[0])
            if idx > 0:
                self.actions[idx-1], self.actions[idx] = self.actions[idx], self.actions[idx-1]
                self._refresh_action_table()
                self.action_table.selection_set(str(idx-1))

    def _move_action_down(self):
        sel = self.action_table.selection()
        if sel:
            idx = int(sel[0])
            if idx < len(self.actions)-1:
                self.actions[idx+1], self.actions[idx] = self.actions[idx], self.actions[idx+1]
                self._refresh_action_table()
                self.action_table.selection_set(str(idx+1))

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
        Uses the action list if present, otherwise falls back to single position/interval.
        """
        if not self.is_clicking:
            run_mode = self.run_mode_var.get()
            actions_to_run = self.actions if self.actions else None
            if actions_to_run:
                # Validate all actions
                for i, act in enumerate(actions_to_run):
                    try:
                        x = int(act["x"])
                        y = int(act["y"])
                        interval = float(act["interval"])
                        if interval <= 0:
                            raise ValueError
                    except Exception:
                        self.label.config(text=f"Invalid action at row {i+1}. Check X, Y, Interval.")
                        return
            # No fallback: all click actions must come from the table

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
            self._executions_done = 0
            # Store clicker config
            if actions_to_run:
                self._click_actions = actions_to_run.copy()
            else:
                self._click_actions = [{
                    "x": self.position[0] if hasattr(self, "position") else int(self.x_entry.get()),
                    "y": self.position[1] if hasattr(self, "position") else int(self.y_entry.get()),
                    "interval": float(self.interval_entry.get()),
                    "type": "click"
                }]
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
        Internal loop that performs mouse actions while is_clicking is True.
        If actions are present, executes them in sequence. Otherwise, uses single position/interval.
        """
        import time
        actions = self._click_actions if hasattr(self, "_click_actions") else None
        run_mode = self.run_mode_var.get()
        executions_limit = self._execution_limit
        executions_done = 0
        duration_mode = (run_mode == "duration")
        start_time = time.time() if duration_mode else None
        while self.is_clicking:
            if actions:
                for idx, act in enumerate(actions):
                    if not self.is_clicking:
                        break
                    x = int(act["x"])
                    y = int(act["y"])
                    interval = float(act["interval"])
                    action_type = act.get("type", "click")
                    # Only support "click" for now
                    if action_type == "click":
                        pyautogui.click(x, y)
                    # Future: support other types
                    self.label.config(text=f"Clicking action {idx+1}/{len(actions)} at ({x},{y})")
                    time.sleep(interval)
                    # Duration mode: stop after time elapsed
                    if duration_mode and (time.time() - start_time) >= self._remaining_time:
                        self.stop_clicking()
                        self.label.config(text="Time is up. Stopped.")
                        return
                # One execution of all actions is done
                executions_done += 1
                # Executions mode: stop after enough actions
                if executions_limit is not None and executions_done >= executions_limit:
                    self.stop_clicking()
                    self.label.config(text=f"Completed {executions_limit} executions.")
                    return
