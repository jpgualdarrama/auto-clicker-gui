import csv
import pyautogui
import time

# --- Action base and registry ---
class BaseAction:
    """
    Base class for all actions. Subclass and implement execute().
    """
    def execute(self, x, y, interval=0.1, repeat=1):
        raise NotImplementedError("Action must implement execute()")

class ClickAction(BaseAction):
    def execute(self, x, y, interval=0.1, repeat=1):
        for _ in range(repeat):
            pyautogui.click(x, y)

class DoubleClickAction(BaseAction):
    def execute(self, x, y, interval=0.1, repeat=1):
        for _ in range(repeat):
            pyautogui.doubleClick(x, y)

# Press and Hold Action (left button only for now)
class PressAndHoldAction(BaseAction):
    def execute(self, x, y, interval=0.1, repeat=1, duration=0.1):
        for _ in range(repeat):
            pyautogui.mouseDown(x, y, button='left')
            time.sleep(duration)
            pyautogui.mouseUp(x, y, button='left')

# Central registry of actions (all keys lowercase)
ACTIONS_REGISTRY = {
    "click": ClickAction,
    "double click": DoubleClickAction,
    "press and hold": PressAndHoldAction,
    # Add new actions here
}

# --- ActionList for managing action data ---
class ActionList:
    """
    Encapsulates management of the list of actions for the Auto Clicker GUI tool.
    Handles add, remove, move, edit, validate, load, and save operations.
    """
    def __init__(self, default_action=None):
        self._actions = []
        if default_action:
            self._actions.append(default_action)

    def add_action(self, action=None):
        if action is None:
            action = {"x": 0, "y": 0, "interval": 0.1, "type": "click", "repeat": 1}
        self._actions.append(action)

    def remove_action(self, idx):
        if 0 <= idx < len(self._actions):
            del self._actions[idx]

    def move_action_up(self, idx):
        if 0 < idx < len(self._actions):
            self._actions[idx-1], self._actions[idx] = self._actions[idx], self._actions[idx-1]

    def move_action_down(self, idx):
        if 0 <= idx < len(self._actions)-1:
            self._actions[idx+1], self._actions[idx] = self._actions[idx], self._actions[idx+1]

    def edit_action(self, idx, col_name, value):
        if 0 <= idx < len(self._actions):
            self._actions[idx][col_name] = value

    def get_actions(self):
        return self._actions

    def set_actions(self, actions):
        self._actions = actions

    def validate_actions(self):
        return all(self.validate_action(act) for act in self._actions)

    def validate_action(self, action):
        try:
            x = int(action["x"])
            y = int(action["y"])
            interval = float(action["interval"])
            repeat = int(action.get("repeat", 1))
            if interval <= 0 or repeat < 1:
                return False
            return True
        except Exception:
            return False

    def load_from_csv(self, file_path):
        actions = []
        try:
            with open(file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if self.validate_action(row):
                        actions.append({
                            "x": int(row["x"]),
                            "y": int(row["y"]),
                            "interval": float(row["interval"]),
                            "type": row["type"].lower(),
                            "repeat": int(row["repeat"])
                        })
                    else:
                        return None, f"Invalid action in CSV."
            self._actions = actions
            return actions, None
        except Exception as e:
            return None, str(e)

    def save_to_csv(self, file_path):
        try:
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["x", "y", "interval", "type", "repeat"])
                writer.writeheader()
                for action in self._actions:
                    writer.writerow(action)
            return None
        except Exception as e:
            return str(e)
