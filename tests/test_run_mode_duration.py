"""
Unit tests for Window run mode selection and duration logic.
Covers:
1. Radio buttons enable/disable duration field
2. Duration is used only when selected
3. Indefinite mode disables duration field and ignores value
4. Timer decrements and stops clicking when time is up
"""
import pytest
from tkinter import Tk
import sys
sys.path.insert(0, 'src')
from gui.window_gui import WindowGUI
from gui.window_logic import WindowLogic

class DummyEntry:
    def __init__(self, value):
        self._value = value
    def get(self):
        return self._value
    def delete(self, start, end):
        self._value = ''
    def insert(self, index, value):
        self._value = value
    def config(self, **kwargs):
        pass

class DummyLabel:
    def __init__(self):
        self.text = ''
    def config(self, **kwargs):
        self.text = kwargs.get('text', self.text)
    def pack(self):
        pass

class DummyMaster:
    def __init__(self):
        self.after_calls = []
    def after(self, ms, func):
        self.after_calls.append((ms, func))

@pytest.fixture
def window(monkeypatch):
    root = Tk()
    win = WindowGUI(root)
    win.duration_entry = DummyEntry('10')
    win.interval_entry = DummyEntry('0.1')
    win.x_entry = DummyEntry('100')
    win.y_entry = DummyEntry('200')
    win.label = DummyLabel()
    win.timer_label = DummyLabel()
    win.master = DummyMaster()
    monkeypatch.setattr(win, 'parse_interval', lambda v: 0.1)
    monkeypatch.setattr(win, 'parse_position', lambda: (100, 200))
    monkeypatch.setattr(win, 'parse_duration', lambda v: 5)
    yield win
    root.destroy()

def test_radio_buttons_enable_disable_duration(window):
    """Radio buttons enable/disable duration field."""
    window.run_mode_var.set('duration')
    window._update_run_mode()
    assert window.duration_entry.config is not None
    window.run_mode_var.set('indefinite')
    window._update_run_mode()
    assert window.duration_entry.config is not None

def test_duration_used_only_when_selected(window):
    """Duration is used only when duration mode is selected."""
    window.run_mode_var.set('duration')
    window.start_clicking()
    assert window._timer_running is True
    assert window._remaining_time == 5

def test_indefinite_mode_disables_duration(window):
    """Indefinite mode disables duration field and ignores value."""
    window.run_mode_var.set('indefinite')
    window.start_clicking()
    assert window._timer_running is False
    assert window._remaining_time == 0

def test_timer_decrements_and_stops(window):
    """Timer decrements and stops clicking when time is up."""
    window.run_mode_var.set('duration')
    window.start_clicking()
    window._timer_running = True
    window._remaining_time = 2
    window.is_clicking = True
    window._update_timer()
    assert window._remaining_time == 1
    window._update_timer()
    assert window._remaining_time == 0
    # Should stop clicking when time is up
    assert window.is_clicking is False
    assert window.label.text == "Time is up. Stopped."
