from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

import pygit2
from attrs import define, field
from path import Path

if not TYPE_CHECKING:
    from rich import print


@define(auto_attribs=True)
class Object:
    @abstractmethod
    def children(self) -> Iterable[Object]:
        raise NotImplementedError("Object.children()")

    @abstractmethod
    def parents(self) -> Iterable[Object]:
        raise NotImplementedError("Object.parents()")


@define(auto_attribs=True)
class Commit(Object):
    pass


@define(auto_attribs=True)
class Tree(Object):
    pass


@define(auto_attribs=True)
class Tag(Object):
    pass


@define(auto_attribs=True)
class Blob(Object):
    pass


@define(auto_attribs=True)
class Reference:
    pass


@define(auto_attribs=True)
class Repo:
    path: Path = field(converter=Path)
    repo: pygit2.repository.Repository = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.repo = pygit2.repository.Repository(str(self.path))

    def dump(self) -> None:
        for oid in self.repo.odb:
            print(f"oid: {oid}")


if __name__ == "__main__":
    print(f"executing: {__file__}")
