from __future__ import annotations

from abc import abstractmethod
from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

import attrs
import pygit2
import pygit2.references
from attrs import define, field
from path import Path

if not TYPE_CHECKING:
    from rich import print

_T = TypeVar("_T")


def buf_len_is_20(inst: Hash, attr: attrs.Attribute[_T], value: _T) -> None:
    sz = len(inst.buf)
    if sz != 20:
        raise ValueError(f"'buf' must be 20 bytes (SHA-1) not {sz}")


@define(auto_attribs=True)
class Hash:
    buf: bytes = field(converter=bytes, validator=buf_len_is_20)

    @property
    def hex(self) -> str:
        return self.buf.hex()

    @classmethod
    def from_str(cls, hex_str: str) -> Self:
        return cls(bytes.fromhex(hex_str))


@define(auto_attribs=True)
class Object:
    @abstractmethod
    def edges_in(self) -> Iterable[Object]:
        raise NotImplementedError("Object.edges_in()")

    @abstractmethod
    def edges_out(self) -> Iterable[Object]:
        raise NotImplementedError("Object.edges_out()")


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
    obj: Object

    @classmethod
    def from_pygit2_ref(cls, pygit2_ref: pygit2.Reference) -> Self:
        return cls(Object())


@define(auto_attribs=True)
class Repo:
    path: Path = field(converter=Path)
    repo: pygit2.repository.Repository = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.repo = pygit2.repository.Repository(str(self.path))

    @property
    def references(self) -> Generator[pygit2.Reference, Any, None]:
        gen = cast(Generator[pygit2.Reference, Any, None], self.repo.references.iterator())
        return gen

    def dump(self) -> None:
        for oid in self.repo.odb:
            print(f"oid: {oid}")


if __name__ == "__main__":
    print(f"executing: {__file__}")
