
"""
Unit tests for Window.parse_position method.
Covers:
1. Valid coordinates within screen bounds
2. Coordinates exceeding screen size (clamped)
3. Negative coordinates (clamped to 0)
4. Invalid input (raises ValueError)
"""
import pytest
import sys
sys.path.insert(0, 'src')
from gui.window_gui import WindowGUI
from gui.window_logic import WindowLogic
from tkinter import Tk

class DummyEntry:
    def __init__(self, value):
        self._value = value
    def get(self):
        return self._value

def test_parse_position_valid_within_bounds(monkeypatch):
    """Should return correct tuple for valid coordinates within screen bounds."""
    root = Tk()
    win = WindowGUI(root)
    win.x_entry = DummyEntry('100')
    win.y_entry = DummyEntry('200')
    monkeypatch.setattr('pyautogui.size', lambda: (1920, 1080))
    assert win.parse_position() == (100, 200)
    root.destroy()

def test_parse_position_x_too_large(monkeypatch):
    """Should clamp x to screen width - 1 if x is too large."""
    root = Tk()
    win = WindowGUI(root)
    win.x_entry = DummyEntry('5000')
    win.y_entry = DummyEntry('100')
    monkeypatch.setattr('pyautogui.size', lambda: (1920, 1080))
    assert win.parse_position() == (1919, 100)
    root.destroy()

def test_parse_position_y_too_large(monkeypatch):
    """Should clamp y to screen height - 1 if y is too large."""
    root = Tk()
    win = WindowGUI(root)
    win.x_entry = DummyEntry('100')
    win.y_entry = DummyEntry('5000')
    monkeypatch.setattr('pyautogui.size', lambda: (1920, 1080))
    assert win.parse_position() == (100, 1079)
    root.destroy()

def test_parse_position_negative(monkeypatch):
    """Should clamp negative coordinates to 0."""
    root = Tk()
    win = WindowGUI(root)
    win.x_entry = DummyEntry('-10')
    win.y_entry = DummyEntry('-20')
    monkeypatch.setattr('pyautogui.size', lambda: (1920, 1080))
    assert win.parse_position() == (0, 0)
    root.destroy()

def test_parse_position_invalid(monkeypatch):
    """Should raise ValueError for non-integer input."""
    root = Tk()
    win = WindowGUI(root)
    win.x_entry = DummyEntry('abc')
    win.y_entry = DummyEntry('def')
    monkeypatch.setattr('pyautogui.size', lambda: (1920, 1080))
    with pytest.raises(ValueError):
        win.parse_position()
    root.destroy()
