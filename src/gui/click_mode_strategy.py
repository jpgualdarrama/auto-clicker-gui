import time
from abc import ABC, abstractmethod

class ClickModeStrategy(ABC):
    @abstractmethod
    def prepare(self, logic):
        pass

    @abstractmethod
    def run(self, logic, actions, action_instances):
        pass

class ExecutionsMode(ClickModeStrategy):
    def _parse_executions(self, value):
        executions = int(value)
        if executions > 0:
            return executions
        raise ValueError("Executions must be a positive integer.")

    def prepare(self, logic):
        try:
            executions = self._parse_executions(logic.gui.executions_entry.get())
        except ValueError:
            logic.gui.label.config(text="Invalid executions. Please enter a positive integer.")
            return False
        logic._timer_running = False
        logic._remaining_time = 0
        logic._execution_limit = executions
        logic._executions_done = 0
        return True

    def run(self, logic, actions, action_instances):
        executions_done = 0
        while logic.is_clicking_event.is_set() and executions_done < logic._execution_limit:
            for idx, act in enumerate(actions):
                if not logic.is_clicking_event.is_set():
                    break
                x = int(act["x"])
                y = int(act["y"])
                interval = float(act["interval"])
                repeat = int(act.get("repeat", 1))
                action_instance = action_instances[idx]
                for r in range(repeat):
                    if not logic.is_clicking_event.is_set():
                        break
                    action_instance.execute(x, y, interval=interval, repeat=1)
                    if logic.is_waiting_event.wait(interval):
                        break
                    logic.gui.label.config(text=f"Running action {idx+1}/{len(actions)} (repeat {r+1}/{repeat}) at ({x},{y})")
            executions_done += 1
        logic.stop_clicking()
        logic.gui.label.config(text=f"Completed {logic._execution_limit} executions.")

class DurationMode(ClickModeStrategy):
    def _parse_duration(self, value):
        duration = int(value)
        if duration > 0:
            return duration
        raise ValueError("Duration must be a positive integer.")

    def prepare(self, logic):
        try:
            duration = self._parse_duration(logic.gui.duration_entry.get())
        except ValueError:
            logic.gui.label.config(text="Invalid duration. Please enter a positive integer.")
            return False
        logic._timer_running = True
        logic._remaining_time = duration
        logic._execution_limit = None
        return True

    def run(self, logic, actions, action_instances):
        start_time = time.time()
        while logic.is_clicking_event.is_set() and (time.time() - start_time) < logic._remaining_time:
            for idx, act in enumerate(actions):
                if not logic.is_clicking_event.is_set():
                    break
                x = int(act["x"])
                y = int(act["y"])
                interval = float(act["interval"])
                repeat = int(act.get("repeat", 1))
                action_instance = action_instances[idx]
                for r in range(repeat):
                    if not logic.is_clicking_event.is_set():
                        break
                    action_instance.execute(x, y, interval=interval, repeat=1)
                    if logic.is_waiting_event.wait(interval):
                        break
                    logic.gui.label.config(text=f"Running action {idx+1}/{len(actions)} (repeat {r+1}/{repeat}) at ({x},{y})")
                if (time.time() - start_time) >= logic._remaining_time:
                    logic.stop_clicking()
                    logic.gui.label.config(text="Time is up. Stopped.")
                    return

class IndefiniteMode(ClickModeStrategy):
    def prepare(self, logic):
        logic._timer_running = False
        logic._remaining_time = 0
        logic._execution_limit = None
        return True

    def run(self, logic, actions, action_instances):
        while logic.is_clicking_event.is_set():
            for idx, act in enumerate(actions):
                if not logic.is_clicking_event.is_set():
                    break
                x = int(act["x"])
                y = int(act["y"])
                interval = float(act["interval"])
                repeat = int(act.get("repeat", 1))
                action_instance = action_instances[idx]
                for r in range(repeat):
                    if not logic.is_clicking_event.is_set():
                        break
                    action_instance.execute(x, y, interval=interval, repeat=1)
                    if logic.is_waiting_event.wait(interval):
                        break
                    logic.gui.label.config(text=f"Running action {idx+1}/{len(actions)} (repeat {r+1}/{repeat}) at ({x},{y})")

def get_click_mode_strategy(mode):
    if mode == "indefinite":
        return IndefiniteMode()
    elif mode == "duration":
        return DurationMode()
    elif mode == "executions":
        return ExecutionsMode()
    return None