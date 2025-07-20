from __future__ import annotations

from typing import ClassVar

from path import Path
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import (
    Footer,
    Header,
    Label,
    Placeholder,
    RichLog,
    TabbedContent,
    TabPane,
    Tree,
)

DEFAULT_ESC_DOUBLE_TAP_MAX_TIME: float = 0.4


class GitObjViewApp(App):
    CSS_PATH = "style.tcss"
    TITLE = "git-objview"
    BINDINGS: ClassVar = [
        ("r", "show_tab('refs')", "References"),
        ("o", "show_tab('objs')", "Objects"),
        ("c", "show_tab('cmts')", "Commits"),
        ("t", "show_tab('tres')", "Trees"),
        ("b", "show_tab('blbs')", "Blobs"),
        ("a", "show_tab('tags')", "Tags"),
        ("q", "quit()", "Quit"),
    ]

    _last_esc_time: float | None

    def __init__(self, *args, git_repo_path: Path | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._git_repo_path = git_repo_path if git_repo_path is not None else Path()
        self._last_esc_time = None

    def compose(self) -> ComposeResult:
        W = Label
        W = Placeholder
        with Container(id="app"):
            yield Header(id="hdr")
            yield Footer(id="ftr")
            with Container(id="main"):
                with TabbedContent(initial="refs", id="browser"):
                    with TabPane("References", id="refs"):
                        yield Tree("refs go here", classes="bview")
                    with TabPane("Objects", id="objs"):
                        yield W("objs go here", classes="bview")
                    with TabPane("Commits", id="cmts"):
                        yield W("cmts go here", classes="bview")
                    with TabPane("Trees", id="tres"):
                        yield W("tres go here", classes="bview")
                    with TabPane("Blobs", id="blbs"):
                        yield W("blbs go here", classes="bview")
                    with TabPane("Tags", id="tags"):
                        with W("tags go here", classes="bview") as t:
                            yield t
                yield W("content goes here", id="content")
        yield RichLog(id="log")

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_id("main").get_child_by_id("browser").active = tab

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
