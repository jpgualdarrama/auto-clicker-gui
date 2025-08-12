from unittest.mock import MagicMock
import tkinter as tk
import sys
sys.path.insert(0, 'src')
from gui.window_gui import WindowGUI

def test_hide_preview_bubbles_destroys_bubbles():
    root = tk.Tk()
    root.withdraw()
    gui = WindowGUI(root)
    mock_bubble1 = MagicMock()
    mock_bubble2 = MagicMock()
    gui.preview_bubbles = [mock_bubble1, mock_bubble2]
    gui.hide_preview_bubbles()
    mock_bubble1.destroy.assert_called_once()
    mock_bubble2.destroy.assert_called_once()
    assert gui.preview_bubbles == []
