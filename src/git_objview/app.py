from datetime import datetime

from path import Path
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Digits, RichLog

DEFAULT_ESC_DOUBLE_TAP_MAX_TIME: float = 0.4


class GitObjViewApp(App):
    CSS = """
    Screen { align: center middle; }
    """

    _last_esc_time: float | None

    def __init__(self, *args, git_repo_path: Path, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._git_repo_path = git_repo_path
        self._last_esc_time = None

    def compose(self) -> ComposeResult:
        yield RichLog()

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(content=event)
        if event.key == "escape":
            if self._last_esc_time is not None:
                if event.time - self._last_esc_time < DEFAULT_ESC_DOUBLE_TAP_MAX_TIME:
                    self.query_one(RichLog).write(content="Got double escape tap, exiting...")
                    self.set_timer(1, lambda: self.exit(None, 0, "<> HAVE <> A <> GREAT <> DAY <>"))
            self._last_esc_time = event.time

    def on_ready(self) -> None:
        # self.update_clock()
        # self.set_interval(1, self.update_clock)
        pass

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")


class GitObjViewAppCwd(GitObjViewApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, git_repo_path=Path(), **kwargs)
