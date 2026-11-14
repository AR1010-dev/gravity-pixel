from nicegui import ui

# Default terminal theme colors
BG_COLOR = "#070b07"
TERMINAL_MAIN = "#4AF626"
TERMINAL_INFO = "#1f6e10"
AMBER = "#FFB000"

_draw_queue = []
_WIDTH = 256
_HEIGHT = 256


def init_terminal(
    width=256, height=256, scanlines=True, glow=True, keep_aspect=True
):
    """Initializes the fullscreen low-res CRT terminal screen."""
    global _WIDTH, _HEIGHT
    _WIDTH = width
    _HEIGHT = height

    fit_rule = "object-fit: contain;" if keep_aspect else ""
    glow_rule = (
        f"filter: drop-shadow(0 0 6px rgba(74, 246, 38, 0.35));" if glow else ""
    )

    scanline_css = ""
    if scanlines:
        scanline_css = """
        body::after {
            content: "";
            position: fixed;
            inset: 0;
            background: repeating-linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0) 0px,
                rgba(0, 0, 0, 0) 2px,
                rgba(0, 0, 0, 0.35) 3px,
                rgba(0, 0, 0, 0.35) 4px
            );
            pointer-events: none;
            z-index: 10;
        }
        """

    ui.add_head_html(f"""
    <style>
        html, body, .nicegui-content {{
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background-color: {BG_COLOR};
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        {scanline_css}
    </style>
    """)

    ui.html(
        f'<canvas id="screen" width="{width}" height="{height}" style="'
        f"width: 100vw; "
        f"height: 100vh; "
        f"{fit_rule} "
        f"display: block; "
        f"background: {BG_COLOR}; "
        f"image-rendering: pixelated; "
        f'{glow_rule}"></canvas>',
        sanitize=False,
    )


def draw_text(text, x, y, color=TERMINAL_MAIN, size=10, align="left"):
    """Draws terminal text at exact (x, y) pixel coordinates."""
    safe_text = str(text).replace("\\", "\\\\").replace('"', '\\"')
    _draw_queue.append(
        f'ctx.fillStyle="{color}"; '
        f'ctx.font="{size}px monospace"; '
        f'ctx.textAlign="{align}"; '
        f'ctx.fillText("{safe_text}", {int(x)}, {int(y)});'
    )


def print_line(
    text, row, col=0, color=TERMINAL_MAIN, size=10, line_height=12, margin=8
):
    """Prints text using terminal row & column grid coordinates (row 0 = top line)."""
    x = margin + (col * (size * 0.6))
    y = margin + size + (row * line_height)
    draw_text(text, x, y, color=color, size=size, align="left")


def draw_cursor(row, col, color=TERMINAL_MAIN, size=10, line_height=12, margin=8):
    """Draws a solid block terminal cursor at a given row and column."""
    char_w = int(size * 0.6)
    x = int(margin + (col * char_w))
    y = int(margin + (row * line_height) + 2)
    _draw_queue.append(
        f'ctx.fillStyle="{color}"; ctx.fillRect({x}, {y}, {char_w}, {size});'
    )


def render():
    """Flushes all queued terminal commands to the browser screen."""
    commands = "\n".join(_draw_queue)
    _draw_queue.clear()

    ui.run_javascript(f"""
        const canvas = document.getElementById("screen");
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        ctx.imageSmoothingEnabled = false;
        ctx.clearRect(0, 0, {_WIDTH}, {_HEIGHT});
        {commands}
    """)
