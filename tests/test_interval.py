"""
Unit tests for Window.parse_interval method.
Covers:
1. Positive integer input
2. Positive float input
3. Negative integer input
4. Non-numeric string input
"""
import sys
import tkinter as tk
sys.path.insert(0, 'src')
from gui.window_gui import WindowGUI
from gui.window_logic import WindowLogic
import pytest

def test_parse_interval_positive_integer():
    """Should return float value for positive integer string."""
    win = WindowGUI(tk.Tk())
    assert win.parse_interval("2") == 2.0

def test_parse_interval_positive_float():
    """Should return float value for positive float string."""
    win = WindowGUI(tk.Tk())
    assert win.parse_interval("0.5") == 0.5

def test_parse_interval_negative_integer():
    """Should raise ValueError for negative integer string."""
    win = WindowGUI(tk.Tk())
    with pytest.raises(ValueError):
        win.parse_interval("-3")

def test_parse_interval_non_numeric():
    """Should raise ValueError for non-numeric string."""
    win = WindowGUI(tk.Tk())
    with pytest.raises(ValueError):
        win.parse_interval("abc")
