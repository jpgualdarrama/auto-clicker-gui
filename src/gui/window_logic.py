import threading
import pyautogui
import keyboard
import time
from tkinter import filedialog, Entry
from .action_list import ActionList

class WindowLogic:
    """
    Handles business logic, event handling, clicker state, and file I/O for the Auto Clicker GUI tool.
    Wires up event handlers to widgets from WindowGUI.
    """
    def __init__(self, gui):
        self.gui = gui
        self.is_clicking_event = threading.Event()
        self.click_thread = None
        self._picking_position = False
        self._execution_limit = None
        self._timer_running = False
        self._remaining_time = 0
        self._executions_done = 0
        default_action = {
            "x": gui.default_mouse_x,
            "y": gui.default_mouse_y,
            "interval": 0.1,
            "type": "click",
            "repeat": 1
        }
        self.action_list = ActionList(default_action)
        self._refresh_action_table()
        # Wire up widget commands
        gui.start_button.config(command=self.start_clicking)
        gui.stop_button.config(command=self.stop_clicking)
        gui.add_action_btn.config(command=self._add_action)
        gui.remove_action_btn.config(command=self._remove_action)
        gui.move_up_btn.config(command=self._move_action_up)
        gui.move_down_btn.config(command=self._move_action_down)
        gui.pick_position_button.config(command=self.enable_position_pick)
        gui.save_actions_btn.config(command=self._save_actions)
        gui.load_actions_btn.config(command=self._load_actions)
        gui.indefinite_radio.config(command=self._update_run_mode)
        gui.duration_radio.config(command=self._update_run_mode)
        gui.executions_radio.config(command=self._update_run_mode)
        gui.action_table.bind("<Double-1>", self._edit_action_cell)
        gui.action_table.bind("<<TreeviewSelect>>", self._on_table_select)
        gui.master.protocol("WM_DELETE_WINDOW", self._on_close)
        self.register_hotkeys()
        self._update_mouse_position_label()

    def _update_mouse_position_label(self):
        try:
            x, y = pyautogui.position()
            self.gui.mouse_position_label.config(text=f"Mouse Position: ({x}, {y})")
        except Exception:
            self.gui.mouse_position_label.config(text="Mouse Position: (error)")
        self.gui.master.after(100, self._update_mouse_position_label)

    def _refresh_action_table(self):
        self.gui.action_table.delete(*self.gui.action_table.get_children())
        for i, action in enumerate(self.action_list.get_actions()):
            self.gui.action_table.insert("", "end", iid=str(i), values=(action["x"], action["y"], action["interval"], action["type"], action["repeat"]))

    def _add_action(self):
        self.action_list.add_action()
        self._refresh_action_table()

    def _remove_action(self):
        sel = self.gui.action_table.selection()
        if sel:
            idx = int(sel[0])
            self.action_list.remove_action(idx)
            self._refresh_action_table()

    def _move_action_up(self):
        sel = self.gui.action_table.selection()
        if sel:
            idx = int(sel[0])
            self.action_list.move_action_up(idx)
            self._refresh_action_table()
            self.gui.action_table.selection_set(str(idx-1))

    def _move_action_down(self):
        sel = self.gui.action_table.selection()
        if sel:
            idx = int(sel[0])
            self.action_list.move_action_down(idx)
            self._refresh_action_table()
            self.gui.action_table.selection_set(str(idx+1))

    def _on_table_select(self, event=None):
        sel = self.gui.action_table.selection()
        if sel:
            self.gui.pick_position_button.config(state="normal")
        else:
            self.gui.pick_position_button.config(state="disabled")

    def _edit_action_cell(self, event):
        region = self.gui.action_table.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.gui.action_table.identify_row(event.y)
        col = self.gui.action_table.identify_column(event.x)
        if not row_id or not col:
            return
        idx = int(row_id)
        col_idx = int(col.replace("#", "")) - 1
        col_name = ("x", "y", "interval", "type", "repeat")[col_idx]
        x0, y0, width, height = self.gui.action_table.bbox(row_id, col)
        edit_win = Entry(self.gui.action_table, width=8)
        edit_win.place(x=x0, y=y0, width=width, height=height)
        edit_win.insert(0, str(self.action_list.get_actions()[idx][col_name]))
        edit_win.focus()
        def save_edit(event=None):
            val = edit_win.get()
            try:
                if col_name in ("x", "y"):
                    val = int(val)
                elif col_name == "interval":
                    val = float(val)
                elif col_name == "repeat":
                    val = int(val)
            except Exception:
                edit_win.destroy()
                return
            self.action_list.edit_action(idx, col_name, val)
            edit_win.destroy()
            self._refresh_action_table()
        edit_win.bind("<Return>", save_edit)
        edit_win.bind("<FocusOut>", lambda e: edit_win.destroy())

    def _save_actions(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        error = self.action_list.save_to_csv(file_path)
        if error:
            self.gui.label.config(text=f"Error saving actions: {error}")
        else:
            self.gui.label.config(text=f"Actions saved to {file_path}")

    def _load_actions(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        actions, error = self.action_list.load_from_csv(file_path)
        if error:
            self.gui.label.config(text=f"Error loading actions: {error}")
            return
        self._refresh_action_table()
        self.gui.label.config(text=f"Actions loaded from {file_path}")

    def _update_run_mode(self):
        mode = self.gui.run_mode_var.get()
        if mode == "duration":
            self.gui.duration_entry.config(state='normal')
            self.gui.executions_entry.config(state='disabled')
        elif mode == "executions":
            self.gui.duration_entry.config(state='disabled')
            self.gui.executions_entry.config(state='normal')
        else:
            self.gui.duration_entry.config(state='disabled')
            self.gui.executions_entry.config(state='disabled')

    def register_hotkeys(self):
        keyboard.add_hotkey('f9', self._on_start_key)
        keyboard.add_hotkey('f10', self._on_stop_key)

    def remove_hotkeys(self):
        keyboard.remove_hotkey('f9')
        keyboard.remove_hotkey('f10')

    def _on_start_key(self, event=None):
        self.start_clicking()
        self.gui.label.config(text="Clicking... (Started via F9)")

    def _on_stop_key(self, event=None):
        self.stop_clicking()
        self.gui.label.config(text="Stopped (via F10)")

    def _on_close(self):
        self.remove_hotkeys()
        self.gui.master.destroy()

    def enable_position_pick(self):
        if not self._picking_position:
            self._picking_position = True
            self.gui.label.config(text="Move mouse to desired position and press F8 (updates selected action)")
            self.gui.master.bind('<F8>', self.set_position_from_mouse)

    def set_position_from_mouse(self, event=None):
        if self._picking_position:
            x, y = pyautogui.position()
            sel = self.gui.action_table.selection()
            if sel:
                idx = int(sel[0])
                self.action_list.edit_action(idx, "x", x)
                self.action_list.edit_action(idx, "y", y)
                self._refresh_action_table()
                self.gui.action_table.selection_set(str(idx))
            self._picking_position = False
            self.gui.master.unbind('<F8>')
            self.gui.label.config(text="Auto Clicker Tool")

    def parse_duration(self, value):
        duration = int(value)
        if duration > 0:
            return duration
        raise ValueError("Duration must be a positive integer.")

    def parse_executions(self, value):
        executions = int(value)
        if executions > 0:
            return executions
        raise ValueError("Executions must be a positive integer.")

    def _update_timer(self):
        if self._timer_running and self.is_clicking_event.is_set():
            self._remaining_time -= 1
            self.gui.label.config(text=f"Clicking... ({self._remaining_time}s left)")
            if self._remaining_time <= 0:
                self.stop_clicking()
                self.gui.label.config(text="Time is up. Stopped.")
            else:
                self.gui.master.after(1000, self._update_timer)

    def start_clicking(self):
        if not self.is_clicking_event.is_set():
            self.is_clicking_event.set()
            run_mode = self.gui.run_mode_var.get()
            actions_to_run = self.action_list.get_actions() if self.action_list.get_actions() else None
            if actions_to_run:
                for i, act in enumerate(actions_to_run):
                    try:
                        x = int(act["x"])
                        y = int(act["y"])
                        interval = float(act["interval"])
                        if interval <= 0:
                            raise ValueError
                    except Exception:
                        self.gui.label.config(text=f"Invalid action at row {i+1}. Check X, Y, Interval.")
                        return
            if run_mode == "duration":
                try:
                    duration = self.parse_duration(self.gui.duration_entry.get())
                except ValueError:
                    self.gui.label.config(text="Invalid duration. Please enter a positive integer.")
                    return
                self._timer_running = True
                self._remaining_time = duration
                self._execution_limit = None
            elif run_mode == "executions":
                try:
                    executions = self.parse_executions(self.gui.executions_entry.get())
                except ValueError:
                    self.gui.label.config(text="Invalid executions. Please enter a positive integer.")
                    return
                self._timer_running = False
                self._remaining_time = 0
                self._execution_limit = executions
            else:
                self._timer_running = False
                self._remaining_time = 0
                self._execution_limit = None
            self.is_clicking = True
            self.gui.label.config(text="Clicking...")
            self._executions_done = 0
            if actions_to_run:
                self._click_actions = [dict(act) for act in actions_to_run]
            else:
                self._click_actions = [{
                    "x": self.gui.default_mouse_x,
                    "y": self.gui.default_mouse_y,
                    "interval": 0.1,
                    "type": "click"
                }]
            self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
            self.click_thread.start()
            if run_mode == "duration":
                self.gui.master.after(1000, self._update_timer)

    def stop_clicking(self):
        self.is_clicking_event.clear()
        self.gui.label.config(text="Stopped")

    def _click_loop(self):
        actions = self._click_actions if hasattr(self, "_click_actions") else None
        run_mode = self.gui.run_mode_var.get()
        executions_limit = self._execution_limit
        executions_done = 0
        duration_mode = (run_mode == "duration")
        start_time = time.time() if duration_mode else None
        while self.is_clicking_event.is_set():
            if actions:
                for idx, act in enumerate(actions):
                    if not self.is_clicking_event.is_set():
                        break
                    x = int(act["x"])
                    y = int(act["y"])
                    interval = float(act["interval"])
                    action_type = act.get("type", "click")
                    repeat = int(act.get("repeat", 1))
                    for r in range(repeat):
                        if not self.is_clicking_event.is_set():
                            break
                        if action_type == "click":
                            pyautogui.click(x, y)
                        # Wait for interval, but break early if is_clicking_event is cleared
                        if not self.is_clicking_event.wait(interval):
                            break
                        self.gui.label.config(text=f"Running action {idx+1}/{len(actions)} (repeat {r+1}/{repeat}) at ({x},{y})")
                        if duration_mode and (time.time() - start_time) >= self._remaining_time:
                            self.stop_clicking()
                            self.gui.label.config(text="Time is up. Stopped.")
                            return
                    if not self.is_clicking_event.is_set():
                        break
                executions_done += 1
                if executions_limit is not None and executions_done >= executions_limit:
                    self.stop_clicking()
                    self.gui.label.config(text=f"Completed {executions_limit} executions.")
                    return
