
import tkinter as tk
from gui.window import Window

def main():
    """
    Entry point for the Auto Clicker GUI tool.
    Initializes Tkinter root and launches the main window.
    """
    root = tk.Tk()
    app = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()