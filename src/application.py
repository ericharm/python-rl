from src.title import Title
import curses


class Application:  # pragma: no cover
    def __init__(self, config):
        self.config = config
        self.states = []
        self.windows = {}

    def run(self, screen):
        self.create_windows(self.config["windows"])
        self.init_title_screen()
        playing = True
        while playing != False:
            self.draw()
            playing = self.handle_input(screen)
            self.states[-1].update()

    def draw(self):
        for state in self.states:
            state.draw(self.windows)
        self.refresh_windows()

    def handle_input(self, keyboard):
        try:
            key_in = keyboard.getkey()
        except:
            key_in = "0"
        return self.states[-1].handle_input(key_in)

    def create_windows(self, window_configs):
        for window in window_configs:
            window_setup = window_configs[window]
            self.windows[window] = curses.newpad(
                window_setup["height"], window_setup["width"]
            )

    def refresh_windows(self):
        window_configs = self.config["windows"]
        for window in window_configs:
            # if window != 'body':
            window_setup = window_configs[window]
            self.windows[window].refresh(
                0,
                0,
                window_setup["y"],
                window_setup["x"],
                curses.LINES - 1,
                curses.COLS - 1,
            )

    def init_title_screen(self):
        title = Title(self.config, self.states)
        self.states.append(title)
