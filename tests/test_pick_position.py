"""
Unit tests for Window position picking logic (button and F8 hotkey).
Covers:
1. Button enables picking mode
2. F8 sets position only when picking mode is enabled
3. F8 does not set position if picking mode is not enabled
"""
import pytest
from src.gui.window import Window
from tkinter import Tk

class DummyEntry:
    def __init__(self, value):
        self._value = value
    def get(self):
        return self._value
    def delete(self, start, end):
        self._value = ''
    def insert(self, index, value):
        self._value = value

def test_enable_position_pick_sets_flag():
    """Button click enables picking mode."""
    root = Tk()
    win = Window(root)
    win.x_entry = DummyEntry('0')
    win.y_entry = DummyEntry('0')
    win._picking_position = False
    win.enable_position_pick()
    assert win._picking_position is True
    root.destroy()

def test_set_position_from_mouse_sets_position(monkeypatch):
    """F8 sets position only when picking mode is enabled."""
    root = Tk()
    win = Window(root)
    win.x_entry = DummyEntry('0')
    win.y_entry = DummyEntry('0')
    win._picking_position = True
    monkeypatch.setattr('pyautogui.position', lambda: (123, 456))
    win.set_position_from_mouse()
    assert win.x_entry.get() == '123'
    assert win.y_entry.get() == '456'
    assert win._picking_position is False
    root.destroy()

def test_set_position_from_mouse_ignored_if_not_picking(monkeypatch):
    """F8 does not set position if picking mode is not enabled."""
    root = Tk()
    win = Window(root)
    win.x_entry = DummyEntry('0')
    win.y_entry = DummyEntry('0')
    win._picking_position = False
    monkeypatch.setattr('pyautogui.position', lambda: (789, 101))
    win.set_position_from_mouse()
    # Should not update entries
    assert win.x_entry.get() == '0'
    assert win.y_entry.get() == '0'
    root.destroy()
