"""
Test cases for execution count mode in Window (auto-clicker GUI).
Covers:
- parse_executions validation
- _click_loop label updates for executions mode
"""
import pytest
from unittest.mock import MagicMock, patch
from src.gui.window import Window

class DummyMaster:
    def __init__(self):
        self.protocol = MagicMock()
        self.title = MagicMock()
        self.after = MagicMock()
        self.bind = MagicMock()
        self.unbind = MagicMock()
        self.destroy = MagicMock()

@pytest.fixture
def window():
    master = DummyMaster()
    win = Window(master)
    # Patch label to avoid Tkinter dependency
    win.label = MagicMock()
    return win

def test_parse_executions_valid(window):
    assert window.parse_executions("5") == 5
    assert window.parse_executions("1") == 1

@pytest.mark.parametrize("val", ["0", "-1", "abc", "", None])
def test_parse_executions_invalid(window, val):
    with pytest.raises(Exception):
        window.parse_executions(val)

@patch("pyautogui.click")
@patch("pyautogui.sleep")
def test_click_loop_updates_label(mock_sleep, mock_click, window):
    window._execution_limit = 3
    window._executions_done = 0
    window.is_clicking = True
    window.position = (0, 0)
    window.interval = 0.01
    # Simulate click loop
    def stop_after():
        window.is_clicking = False
    window.stop_clicking = stop_after
    window.label.config = MagicMock()
    window._click_loop()
    # Should call label.config with executions left
    calls = [call[0][0] for call in window.label.config.call_args_list]
    assert any("executions left" in c for c in calls)
    assert any("Completed" in c for c in calls)
