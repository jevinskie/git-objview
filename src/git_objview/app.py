from path import Path
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import (
    Header,
    Placeholder,
    RichLog,
    TabbedContent,
    TabPane,
)

DEFAULT_ESC_DOUBLE_TAP_MAX_TIME: float = 0.4


class GitObjViewApp(App):
    CSS_PATH = "style.tcss"
    TITLE = "git-objview"

    _last_esc_time: float | None

    def __init__(self, *args, git_repo_path: Path | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._git_repo_path = git_repo_path if git_repo_path is not None else Path()
        self._last_esc_time = None

    def compose(self) -> ComposeResult:
        with Vertical(id="main"):
            yield Header(show_clock=True, id="hdr")
            with TabbedContent(id="browser"):
                with TabPane("References", id="refs"):
                    yield Placeholder("refs go here")
                with TabPane("Objects", id="objs"):
                    yield Placeholder("objs go here")
                with TabPane("Commits", id="cmts"):
                    yield Placeholder("cmts go here")
                with TabPane("Trees", id="tres"):
                    yield Placeholder("tres go here")
                with TabPane("Blobs", id="blbs"):
                    yield Placeholder("blbs go here")
                with TabPane("Tags", id="tags"):
                    yield Placeholder("tags go here")
        yield RichLog(id="log")

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
