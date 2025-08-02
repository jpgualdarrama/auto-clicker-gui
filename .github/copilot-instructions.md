# Copilot Instructions for Auto Clicker GUI Tool

## Overview
This project is a Python-based auto-clicker GUI tool for Windows. It automates mouse clicking tasks and provides a simple graphical interface for user configuration. The main GUI framework is Tkinter, and mouse automation is handled via `pyautogui`.

## Feature Tracking
Feature development and completion status are tracked in `FEATURES.md` in the project root. Use this file to view, add, or mark features as complete. Features are managed as a checklist for easy progress tracking.

## Architecture
- **Entry Point:** `src/main.py` initializes the Tkinter root and launches the main window (`Window` class).
- **GUI Logic:** `src/gui/window.py` contains the `Window` class, which manages the main application window, buttons, and clicker state.
- **Dependencies:** All required packages are listed in `requirements.txt`. Key dependencies: `tkinter`, `pyautogui`, `pillow`.

## Developer Workflows
- **Run the App:**
  ```bash
  python src/main.py
  ```
- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- **Debugging:**
  - Use print statements or Tkinter label updates for quick feedback.
  - GUI changes are reflected by editing `window.py`.
- **Documentation**
  - Add documentation comments in the code using standard formats (e.g., docstrings).
  - Update `README.md` for user-facing documentation.
- **Testing:**
  - After making changes, run the app to ensure the GUI still behaves as expected.
  - Add unit tests for new code using pytest.
  - Check that code coverage is maintained at 90% or higher.
  - Run pylint on the codebase to ensure style and quality standards are met.

## Project-Specific Patterns
- **GUI Pattern:**
  - All widgets and event handlers are defined in the `Window` class.
  - Use `self.is_clicking` to track clicker state.
  - Start/Stop buttons update both state and label text.
- **Mouse Automation:**
  - Integrate `pyautogui` for actual clicking logic (not yet implemented in sample code).
  - Add click interval and position controls as needed.

## Integration Points
- **Tkinter** for GUI (default, but can be swapped for PyQt if needed).
- **pyautogui** for mouse automation (ensure Windows compatibility).

## Conventions
- All source code is under `src/`.
- GUI code is isolated in `src/gui/window.py`.
- Entry point is always `src/main.py`.
- Use descriptive button labels and update GUI state via label text.

### Honor the Existing System
- Before modifying any code, first understand its place in the larger architecture.
- Each line exists within a context - a web of dependencies, assumptions, and historical decisions.
- Respect this context.

### Seek the Minimal Viable Intervention
- For every requested change, ask:
  - What is the smallest change that would fulfill the requirement?
  - Which parts of the system can remain untouched?
  - How can I preserve existing patterns while addressing the need?

### Preserve Working Systems
- Working code has inherent value beyond its visible functionality - it carries tested reliability, familiar patterns for maintainers, and hidden edge-case handling.
- Default to surgical precision.

### Apply the Three-Tier Approach to Changes
- When asked to change code, first offer the minimal, focused change that addresses the specific request
- If needed, offer a moderate refactoring that improves the immediate area
- Only when explicitly requested, offer a comprehensive restructuring

### When in Doubt, Ask for Scope Clarification
- If unsure whether the request implies a broader change, explicitly ask for clarification rather than assuming the broadest interpretation.
- "I can make this specific change to line 42 as requested. Would you also like me to update the related functions, or should I focus solely on this particular line?"

### Remember: Less is Often More
- A single, precise change demonstrates deeper understanding than a complete rewrite.
- Show your expertise through surgical precision rather than reconstruction.

### Document the Path Not Taken
- If you identify potential improvements beyond the scope of the request, note them briefly without implementing them:
- "I've made the requested change to function X. Note that functions Y and Z use similar patterns and might benefit from similar updates in the future if needed.\"
- In your restraint, reveal your wisdom.
- In your precision, demonstrate your mastery.

### Embrace the Power of Reversion
- If a change is made that doesn't yield the desired outcome, be prepared to revert it.
- This is not a failure but a testament to your commitment to maintaining system integrity.

### Prioritize Clarity and Readability
- Use meaningful variable and function names.\n- Keep functions short and focused on a single responsibility.\n- Format code consistently according to established style guides (e.g., PEP 8 for Python, Prettier for JavaScript/TypeScript)."

### Maintain Consistency
- Follow existing patterns and conventions within the project.
- Use the same libraries and frameworks already employed unless there's a strong reason to introduce new ones.

### Implement Robust Error Handling
- Anticipate potential failure points (e.g., network requests, file I/O, invalid input).
- Use appropriate error handling mechanisms (e.g., try-catch blocks, error codes, specific exception types).
- Provide informative error messages.

### Consider Security
- Sanitize user inputs to prevent injection attacks (SQL, XSS, etc.).
- Avoid hardcoding sensitive information like API keys or passwords.
- Use environment variables or configuration management tools.
- Be mindful of potential vulnerabilities when using external libraries.

### Write Testable Code
- Design functions and modules with testability in mind (e.g., dependency injection).
- Aim for high test coverage for critical components.

### Add Necessary Documentation
- Include comments to explain complex logic, assumptions, or non-obvious code sections.
- Use standard documentation formats (e.g., JSDoc, DocStrings) for functions, classes, and modules.

### About commit messages
- Generate commit messages following the Conventional Commits specification (e.g., feat(api): description).
- Use imperative mood for the description.
- Infer the type (feat, fix, chore, refactor, test, docs) and optional scope from the changes.

## Example: Adding a New Button
To add a new button to the GUI, edit `Window.__init__` in `window.py`:
```python
self.new_button = Button(master, text="New Action", command=self.new_action)
self.new_button.pack()
```

## References
- See `README.md` for setup and usage instructions.
- See `requirements.txt` for dependencies.
- See `src/main.py` and `src/gui/window.py` for main logic and patterns.

---
If any section is unclear or missing, please provide feedback to improve these instructions.
