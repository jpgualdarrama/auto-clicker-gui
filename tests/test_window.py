"""
Unit tests for Window class auto-clicker logic.
"""
import pytest
from unittest.mock import patch
import threading
import time
import sys
import tkinter as tk

sys.path.insert(0, 'src')
from gui.window import Window


def test_start_stop_clicking(monkeypatch):
    master = tk.Tk()
    master.withdraw()  # Hide the window during tests
    win = Window(master)
    # Patch pyautogui.click and pyautogui.sleep
    monkeypatch.setattr('pyautogui.click', lambda: None)
    monkeypatch.setattr('pyautogui.sleep', lambda x: time.sleep(0.01))

    win.start_clicking()
    assert win.is_clicking is True
    time.sleep(0.05)
    win.stop_clicking()
    assert win.is_clicking is False
    # Ensure thread stops
    if win.click_thread:
        win.click_thread.join(timeout=0.1)
        assert not win.click_thread.is_alive()
