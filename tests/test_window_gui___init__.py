import pytest
import tkinter as tk
import sys
sys.path.insert(0, 'src')
from gui.window_gui import WindowGUI

def test_init_creates_widgets():
    root = tk.Tk()
    root.withdraw()
    gui = WindowGUI(root)
    assert hasattr(gui, 'label')
    assert hasattr(gui, 'start_button')
    assert hasattr(gui, 'stop_button')
    assert hasattr(gui, 'action_table')
    assert gui.label.cget('text') == "Auto Clicker Tool"
    assert gui.default_mouse_x is not None
    assert gui.default_mouse_y is not None
