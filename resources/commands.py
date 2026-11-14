import json
from pathlib import Path
import time
from resources import rendering as term

current_input = ""
history = []  # Stores tuples of (text, color)
MAX_COLS = 40

COMMANDS_FILE = Path(__file__).parent / "commands.json"

COLOR_MAP = {
    "main": term.TERMINAL_MAIN,
    "info": term.TERMINAL_INFO,
    "amber": term.AMBER,
}


def _load_commands():
    """Reads commands.json from disk so edits apply immediately without restarting."""
    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"_error": {"text": f"JSON ERROR: {e}", "color": "amber"}}


def _wrap_text(text, width=MAX_COLS):
    """Splits a string into chunks of `width` characters so nothing goes offscreen."""
    if not text:
        return [""]
    return [text[i : i + width] for i in range(0, len(text), width)]


def _add_response(text, color=term.TERMINAL_MAIN):
    """Wraps long command responses cleanly onto multiple rows."""
    for line in _wrap_text(text):
        history.append((line, color))


def handle_key(key):
    """Called every time a key is pressed on the keyboard."""
    global current_input

    if key == "Backspace":
        current_input = current_input[:-1]
    elif key == "Enter":
        cmd = current_input.strip()
        for line in _wrap_text(f"> {current_input}"):
            history.append((line, term.TERMINAL_MAIN))
        current_input = ""
        if cmd:
            run_command(cmd)
    elif len(key) == 1:
        current_input += key


def run_command(cmd):
    """Looks up the typed command inside commands.json and runs its response."""
    commands_data = _load_commands()
    entry = commands_data.get(cmd.lower())

    if not entry:
        _add_response(f"UNKNOWN CMD: {cmd}", term.AMBER)
        return

    # Handle special actions like clearing the terminal
    if entry.get("action") == "clear":
        history.clear()
        return

    # Resolve color name from JSON (defaults to TERMINAL_MAIN)
    color_key = entry.get("color", "main").lower()
    color = COLOR_MAP.get(color_key, color_key)

    # Support either a single string or a list of lines in JSON
    text_data = entry.get("text", "")
    if isinstance(text_data, list):
        for line in text_data:
            _add_response(line, color)
    else:
        _add_response(text_data, color)


def draw_prompt(start_row):
    """Renders wrapped history, wrapped active typing, and the moving cursor."""
    row = start_row

    for line_text, line_color in history[-8:]:
        term.print_line(line_text, row=row, color=line_color)
        row += 1

    prompt_text = f"> {current_input}"
    wrapped_lines = _wrap_text(prompt_text)

    for i, line in enumerate(wrapped_lines):
        term.print_line(line, row=row + i, color=term.TERMINAL_MAIN)

    last_line = wrapped_lines[-1]
    cursor_row = row + len(wrapped_lines) - 1
    cursor_col = len(last_line)

    if cursor_col >= MAX_COLS:
        cursor_row += 1
        cursor_col = 0

    if int(time.time() * 2) % 2 == 0:
        term.draw_cursor(row=cursor_row, col=cursor_col)
