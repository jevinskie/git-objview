from __future__ import annotations

from typing import TYPE_CHECKING

import pygit2
from attrs import define, field
from path import Path

if not TYPE_CHECKING:
    from rich import print


@define(auto_attribs=True)
class Repo:
    path: Path = field(converter=Path)
    repo: pygit2.repository.Repository = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.repo = pygit2.repository.Repository(str(self.path))

    def dump(self) -> None:
        for oid in self.repo.odb:
            print(f"oid: {oid}")
