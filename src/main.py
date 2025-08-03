
import tkinter as tk
from gui.window_gui import WindowGUI
from gui.window_logic import WindowLogic

def main():
    """
    Entry point for the Auto Clicker GUI tool.
    Initializes Tkinter root and launches the main window.
    """
    root = tk.Tk()
    gui = WindowGUI(root)
    logic = WindowLogic(gui)
    root.mainloop()

if __name__ == "__main__":
    main()