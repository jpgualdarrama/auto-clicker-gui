from tkinter import Label, Button, Entry, Radiobutton, StringVar, ttk, Toplevel, Canvas
import pyautogui

class WindowGUI:
    """
    Handles creation and layout of all Tkinter widgets for the Auto Clicker GUI tool.
    Exposes widget references for use by logic/controller classes.
    """
    def __init__(self, master):
        self.master = master
        master.title("Auto Clicker")

        self.label = Label(master, text="Auto Clicker Tool")
        self.label.pack()

        self.mouse_position_label = Label(master, text="Mouse Position: (0, 0)", font=("Segoe UI", 9))
        self.mouse_position_label.pack(pady=(2,0))
        # Mouse position updating logic will be handled by logic/controller

        self.start_stop_frame = ttk.Frame(master)
        self.start_stop_frame.pack(pady=(4,0))
        self.start_button = Button(self.start_stop_frame, text="Start (F9)")
        self.start_button.grid(row=0, column=0, padx=2)
        self.stop_button = Button(self.start_stop_frame, text="Stop (F10)")
        self.stop_button.grid(row=0, column=1, padx=2)

        mouse_x, mouse_y = pyautogui.position()

        self.run_mode_var = StringVar(value="indefinite")
        self.run_mode_frame = ttk.Frame(master)
        self.run_mode_frame.pack(pady=(8,0))
        self.indefinite_radio = Radiobutton(self.run_mode_frame, text="Run Indefinitely", variable=self.run_mode_var, value="indefinite")
        self.indefinite_radio.grid(row=0, column=0, padx=4)
        self.duration_radio = Radiobutton(self.run_mode_frame, text="Run for Duration", variable=self.run_mode_var, value="duration")
        self.duration_radio.grid(row=0, column=1, padx=4)
        self.executions_radio = Radiobutton(self.run_mode_frame, text="Run for Number of Executions", variable=self.run_mode_var, value="executions")
        self.executions_radio.grid(row=0, column=2, padx=4)

        self.duration_label = Label(self.run_mode_frame, text="Duration (seconds):")
        self.duration_label.grid(row=1, column=1, pady=(2,0))
        self.duration_entry = Entry(self.run_mode_frame)
        self.duration_entry.insert(0, "10")
        self.duration_entry.grid(row=2, column=1)
        self.duration_entry.config(state='disabled')

        self.executions_label = Label(self.run_mode_frame, text="Number of Executions:")
        self.executions_label.grid(row=1, column=2, pady=(2,0))
        self.executions_entry = Entry(self.run_mode_frame)
        self.executions_entry.insert(0, "100")
        self.executions_entry.grid(row=2, column=2)
        self.executions_entry.config(state='disabled')

        self.action_table_label = Label(master, text="Action List", font=("Segoe UI", 10, "bold"))
        self.action_table_label.pack(pady=(10,0))
        self.action_table = ttk.Treeview(master, columns=("x", "y", "interval", "type", "repeat"), show="headings", selectmode="browse", height=6)
        for col in ("x", "y", "interval", "type", "repeat"):
            self.action_table.heading(col, text=col.capitalize())
            self.action_table.column(col, width=80, anchor="center")
        self.action_table.pack(pady=8)

        self.action_controls_frame = ttk.Frame(master)
        self.action_controls_frame.pack()
        self.add_action_btn = Button(self.action_controls_frame, text="Add")
        self.add_action_btn.grid(row=0, column=0, padx=2)
        self.remove_action_btn = Button(self.action_controls_frame, text="Remove")
        self.remove_action_btn.grid(row=0, column=1, padx=2)
        self.move_up_btn = Button(self.action_controls_frame, text="Move Up")
        self.move_up_btn.grid(row=0, column=2, padx=2)
        self.move_down_btn = Button(self.action_controls_frame, text="Move Down")
        self.move_down_btn.grid(row=0, column=3, padx=2)
        self.pick_position_button = Button(self.action_controls_frame, text="Pick Position (F7)", state="disabled")
        self.pick_position_button.grid(row=0, column=4, padx=2)

        self.save_load_frame = ttk.Frame(master)
        self.save_load_frame.pack()
        self.save_actions_btn = Button(self.save_load_frame, text="Save Actions")
        self.save_actions_btn.grid(row=0, column=0, padx=2)
        self.load_actions_btn = Button(self.save_load_frame, text="Load Actions")
        self.load_actions_btn.grid(row=0, column=1, padx=2)

        # Expose mouse_x, mouse_y for default action
        self.default_mouse_x = mouse_x
        self.default_mouse_y = mouse_y
        # Preview bubbles state and button
        self.preview_enabled = False
        self.preview_bubbles = []
        self.preview_button = Button(master, text="Enable Preview (F8)", command=self.toggle_preview)
        self.preview_button.pack(pady=(8,0))

    def toggle_preview(self):
        self.preview_enabled = not self.preview_enabled
        self.preview_button.config(text=("Disable Preview (F8)" if self.preview_enabled else "Enable Preview (F8)"))
        if self.preview_enabled:
            self.show_preview_bubbles()
        else:
            self.hide_preview_bubbles()

    def show_preview_bubbles(self, positions=None):
        """
        Show semi-transparent bubbles at given positions. If positions is None, use all actions in table.
        """
        self.hide_preview_bubbles()
        if positions is None and hasattr(self, 'action_table'):
            positions = []
            for item in self.action_table.get_children():
                vals = self.action_table.item(item, 'values')
                if len(vals) >= 2:
                    try:
                        x, y = int(vals[0]), int(vals[1])
                        positions.append((x, y))
                    except Exception:
                        continue
        for x, y in positions:
            bubble = self._create_bubble(x, y)
            self.preview_bubbles.append(bubble)

    def hide_preview_bubbles(self):
        for bubble in self.preview_bubbles:
            try:
                bubble.destroy()
            except Exception:
                pass
        self.preview_bubbles = []

    def _create_bubble(self, x, y, size=40, alpha=0.4):
        """
        Create a semi-transparent Toplevel window as a bubble overlay at (x, y).
        """
        bubble = Toplevel(self.master)
        bubble.overrideredirect(True)
        bubble.attributes('-topmost', True)
        bubble.attributes('-alpha', alpha)
        bubble.wm_attributes('-transparentcolor','#000000')
        bubble.geometry(f"{size}x{size}+{x-size//2}+{y-size//2}")
        # Draw a circle using Canvas
        canvas = Canvas(bubble, width=size, height=size, highlightthickness=0, bg='#000000')
        canvas.pack()
        # Draw filled circle (bubble) with border
        circle_color = '#00aaff'  # Light blue, can be changed
        border_color = '#005577'  # Darker blue for border
        border_width = 2
        canvas.create_oval(border_width, border_width, size-border_width, size-border_width,
                          fill=circle_color, outline=border_color, width=border_width)
        # Draw crosshairs
        crosshair_color = '#ffffff'  # White crosshairs
        crosshair_width = 2
        center = size // 2
        offset = size // 4
        # Vertical line
        canvas.create_line(center, border_width, center, size-border_width, fill=crosshair_color, width=crosshair_width)
        # Horizontal line
        canvas.create_line(border_width, center, size-border_width, center, fill=crosshair_color, width=crosshair_width)
        return bubble
