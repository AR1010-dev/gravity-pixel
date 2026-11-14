from nicegui import ui
from resources import commands
from resources import rendering as term

term.init_terminal(width=256, height=256, scanlines=True, glow=True)
term.bind_keyboard(commands.handle_key)


def update_frame():
    term.print_timed("Loading...", row=0, delay=0.0, type_speed=0.05, color=term.TERMINAL_INFO)
    term.print_timed("NBJAT v0.01b [READY]", row=term.last_row, delay=1.0, type_speed=0.04, color=term.TERMINAL_INFO)
    term.print_timed("------------------------", row=term.last_row + 1, delay=0.2, type_speed=0.01, color=term.TERMINAL_INFO)
    term.print_timed("> INIT NBJAT...", row=term.last_row + 2, delay=0.4, type_speed=0.04)
    done = term.print_timed("> STATUS: ONLINE", row=term.last_row + 1, delay=0.5, type_speed=0.04)

    # Once boot finishes, hand control over to your commands.py prompt
    if done:
        commands.draw_prompt(start_row=term.last_row + 2)

    term.render()


ui.timer(0.016, update_frame)
ui.run(port=8000, show=False)
