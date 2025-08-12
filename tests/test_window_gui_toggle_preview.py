import pytest
from unittest.mock import MagicMock
import tkinter as tk
import sys
sys.path.insert(0, 'src')
from gui.window_gui import WindowGUI

def test_toggle_preview_toggles_state_and_button(monkeypatch):
    root = tk.Tk()
    root.withdraw()
    gui = WindowGUI(root)
    gui.show_preview_bubbles = MagicMock()
    gui.hide_preview_bubbles = MagicMock()
    # Initially disabled
    assert gui.preview_enabled is False
    gui.toggle_preview()
    assert gui.preview_enabled is True
    gui.show_preview_bubbles.assert_called_once()
    assert "Disable Preview" in gui.preview_button.cget('text')
    gui.toggle_preview()
    assert gui.preview_enabled is False
    gui.hide_preview_bubbles.assert_called_once()
    assert "Enable Preview" in gui.preview_button.cget('text')
