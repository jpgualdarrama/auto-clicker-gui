from unittest.mock import MagicMock
import tkinter as tk
import sys
sys.path.insert(0, 'src')
from gui.window_gui import WindowGUI

def test_show_preview_bubbles_creates_bubbles():
    root = tk.Tk()
    root.withdraw()
    gui = WindowGUI(root)
    gui._create_bubble = MagicMock(return_value=MagicMock())
    positions = [(10, 10), (20, 20)]
    gui.show_preview_bubbles(positions)
    assert len(gui.preview_bubbles) == 2
    gui._create_bubble.assert_any_call(10, 10)
    gui._create_bubble.assert_any_call(20, 20)
