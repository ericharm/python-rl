import curses
from typing import Optional

class State:
    def draw(self, windows: dict[str, curses.window]) -> None:
        pass

    def handle_input(self, key: str) -> Optional[bool]:
        return True

    def update(self) -> bool:
        return True
