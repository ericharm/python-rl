from src.state import State
from src.title import Title
from src.window_config import WindowConfig
import curses

class Application:  # pragma: no cover
    def __init__(self, config: dict):
        self.config = config
        self.states: list[State] = []
        self.windows: dict[str, curses.window] = {}

    def run(self, screen: curses.window) -> None:
        self.create_windows(self.config["windows"])
        self.init_title_screen()
        playing = True
        while playing != False:
            self.draw()
            playing = self.handle_input(screen)
            self.states[-1].update()

    def draw(self) -> None:
        for state in self.states:
            state.draw(self.windows)
        self.refresh_windows()

    def handle_input(self, keyboard: curses.window) -> bool:
        try:
            key_in = keyboard.getkey()
        except:
            key_in = "0"
        return self.states[-1].handle_input(key_in)

    def create_windows(self, window_configs: dict[str, WindowConfig]) -> None:
        for window in window_configs:
            window_setup = window_configs[window]
            self.windows[window] = curses.newpad(
                window_setup["height"], window_setup["width"]
            )

    def refresh_windows(self) -> None:
        window_configs = self.config["windows"]
        for window in window_configs:
            window_setup = window_configs[window]
            self.windows[window].refresh(
                0,
                0,
                window_setup["y"],
                window_setup["x"],
                curses.LINES - 1,
                curses.COLS - 1,
            )

    def init_title_screen(self) -> None:
        title = Title(self.config, self.states)
        self.states.append(title)
