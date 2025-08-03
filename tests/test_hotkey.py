"""
Unit tests for global hotkey integration in Window class.
Covers:
1. Hotkey registration and removal
2. Hotkey triggers start/stop methods
3. Label updates on hotkey press
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, 'src')
from gui.window import Window

# Dummy master to avoid real Tkinter window creation

class DummyMaster:
    def __init__(self):
        self.protocol_calls = []
    def title(self, text):
        pass
    def protocol(self, name, func):
        self.protocol_calls.append((name, func))
    def bind(self, *args, **kwargs):
        pass
    def unbind(self, *args, **kwargs):
        pass
    def destroy(self):
        pass
    def after(self, ms, func):
        pass

class DummyLabel:
    def __init__(self):
        self.text = ""
    def config(self, **kwargs):
        self.text = kwargs.get('text', self.text)
    def cget(self, key):
        if key == 'text':
            return self.text
        return None

class DummyButton:
    def pack(self):
        pass

class DummyEntry:
    def __init__(self, value="0"):
        self._value = value
    def get(self):
        return self._value
    def insert(self, index, value):
        self._value = value
    def delete(self, start, end):
        self._value = ""
    def config(self, **kwargs):
        pass


@pytest.fixture
def window(monkeypatch):
    monkeypatch.setattr('keyboard.add_hotkey', lambda key, func: None)
    monkeypatch.setattr('keyboard.remove_hotkey', lambda key: None)
    monkeypatch.setattr(Window, 'register_hotkeys', lambda self: None)
    monkeypatch.setattr(Window, 'remove_hotkeys', lambda self: None)
    win = Window(DummyMaster())
    # Patch widgets with dummy objects
    win.label = DummyLabel()
    win.start_button = DummyButton()
    win.stop_button = DummyButton()
    win.interval_label = DummyLabel()
    win.interval_entry = DummyEntry('0.1')
    win.x_label = DummyLabel()
    win.x_entry = DummyEntry('100')
    win.y_label = DummyLabel()
    win.y_entry = DummyEntry('200')
    win.pick_position_button = DummyButton()
    win.duration_label = DummyLabel()
    win.duration_entry = DummyEntry('10')
    win.indefinite_radio = DummyButton()
    win.duration_radio = DummyButton()
    yield win

def test_hotkey_registration_and_removal(monkeypatch):
    """Should call add_hotkey and remove_hotkey for F9/F10."""
    add_calls = []
    remove_calls = []
    monkeypatch.setattr('keyboard.add_hotkey', lambda key, func: add_calls.append(key))
    monkeypatch.setattr('keyboard.remove_hotkey', lambda key: remove_calls.append(key))
    monkeypatch.setattr(Window, 'register_hotkeys', lambda self: None)
    monkeypatch.setattr(Window, 'remove_hotkeys', lambda self: None)
    win = Window(DummyMaster())
    win.label = DummyLabel()
    win._on_close()
    assert 'f9' in add_calls
    assert 'f10' in add_calls
    assert 'f9' in remove_calls
    assert 'f10' in remove_calls

def test_hotkey_triggers_start_stop(window):
    """Should call start_clicking and stop_clicking on hotkey press."""
    window.is_clicking = False
    with patch.object(window, 'start_clicking') as start_mock:
        window._on_start_key()
        start_mock.assert_called_once()
    with patch.object(window, 'stop_clicking') as stop_mock:
        window._on_stop_key()
        stop_mock.assert_called_once()

def test_label_updates_on_hotkey(window):
    """Should update label text on hotkey press."""
    window._on_start_key()
    assert "Started via F9" in window.label.cget('text')
    window._on_stop_key()
    assert "via F10" in window.label.cget('text')
