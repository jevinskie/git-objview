from path import Path
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, RichLog, Static, Tree

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
        yield Header()
        yield RichLog()
        with Horizontal():
            with Vertical(classes="column"):
                yield RichLog()
                yield Static("Two")
            with Vertical(classes="column"):
                yield Static("Three")
                yield Tree("treez")
        yield Footer()

    def do_exit(self, message: str = "<> HAVE <> A <> GREAT <> DAY <>") -> None:
        self.exit(None, 0, message)

    def handle_exit_requests(self, event: events.Key) -> None:
        if event.key == "escape":
            if self._last_esc_time is not None:
                if event.time - self._last_esc_time < DEFAULT_ESC_DOUBLE_TAP_MAX_TIME:
                    self.query_one(RichLog).write(content="Got double escape tap, exiting...")
                    self.set_timer(1, self.do_exit)
            self._last_esc_time = event.time

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(content=event)
        self.handle_exit_requests(event)

    def on_ready(self) -> None:
        pass


class GitObjViewAppCwd(GitObjViewApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, git_repo_path=Path(), **kwargs)
