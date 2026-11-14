import time
from nicegui import ui
from resources import rendering as term

term.init_terminal(width=256, height=256, scanlines=True, glow=True)

def update_frame():
    # Print text by terminal row (0, 1, 2...) just like a real console
    term.print_line("NBJAT v0.01a [READY]", row=0, color=term.TERMINAL_INFO) # NBJAT stands for No Builders Just A Tool
    term.print_line("------------------------", row=1, color=term.TERMINAL_INFO)
    term.print_line("> INIT GRAVITY PIXEL...", row=3, color=term.TERMINAL_MAIN)
    term.print_line("> STATUS: ONLINE", row=4, color=term.TERMINAL_MAIN)

    # Blinking block cursor every 0.5 seconds
    if int(time.time() * 2) % 2 == 0:
        term.draw_cursor(row=6, col=0)

    # Push frame to screen
    term.render()


ui.timer(0.016, update_frame)
ui.run(port=8000, show=False)
