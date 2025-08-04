# TODOS

**Note:** Always add new TODOs to this file for tracking.

- [ ] Fix bug with hotkeys being disabled after Stop Clicking was clicked when the tool was clicking inside the GUI.
  - Doesn't occur with clicks outside of the GUI.
  - When the Start Clicking button is clicked (after Stop Clicking) was clicked, on_start_clicking gets part of the way through, but it hangs before setting the label. It hangs until the GUI is clicked manually, then it proceeds.

- [ ] Refactor Window.__init__ to allow dependency injection of widgets for easier testing (e.g., pass widget factories or dummy widgets)
- [ ] Fix test_start_stop_clicking in tests/test_window.py: Tkinter/TclError due to missing or misconfigured Tk installation. Ensure Tk is properly installed and available in the test environment.

# Hotkey Feature Refactor TODOs
- [ ] Refactor hotkey logic into a separate helper class/module (e.g., HotkeyManager)
- [ ] Abstract position selection logic in Window (e.g., set_click_position)
- [ ] Add status messages/label for hotkey feedback and errors
- [ ] Support configurable hotkeys in the GUI
- [ ] Add unit tests for hotkey logic
- [ ] Add clear documentation for hotkey integration and platform specifics
