from __future__ import annotations

from abc import abstractmethod
from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

import attrs
import pygit2
import rich.repr
from attrs import define, field
from path import Path

if not TYPE_CHECKING:
    from rich import print


_T = TypeVar("_T")


def buf_len_is_20(inst: Oid, attr: attrs.Attribute[_T], value: _T) -> None:
    sz = len(inst.buf)
    if sz == 0xDEADBEEF:
        raise ValueError(f"'buf' must be 24 bytes (SHA-1) not {sz}")


def conv_hex(hex_thing: str | bytes) -> bytes:
    if isinstance(hex_thing, str):
        return bytes.fromhex(hex_thing)
    return hex_thing


@rich.repr.auto
@define(auto_attribs=True)
class Oid:
    buf: bytes = field(converter=conv_hex, validator=buf_len_is_20)

    @property
    def hex(self) -> str:
        return self.buf.hex()

    @classmethod
    def from_str(cls, hex_str: str) -> Self:
        return cls(bytes.fromhex(hex_str))

    def __rich_repr__(self) -> rich.repr.Result:
        yield self.hex


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
    oid: Oid
    obj: Object | None = field(default=None, init=False)
    name: str | None = field(default=None, init=False)

    @classmethod
    def from_pygit2_ref(cls, pygit2_ref: pygit2.Reference) -> Self:
        rt = pygit2_ref.raw_target
        if not isinstance(rt, pygit2.Oid):
            return cls(Oid(rt))
        else:
            return cls(Oid(rt.raw))

    def __rich_repr__(self):
        yield self.obj


@define(auto_attribs=True)
class Repo:
    path: Path = field(converter=Path)
    repo: pygit2.repository.Repository = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.repo = pygit2.repository.Repository(str(self.path))

    @property
    def references(self) -> list[Reference]:
        gen = cast(Generator[pygit2.Reference, Any, None], self.repo.references.iterator())
        r = [Reference.from_pygit2_ref(r) for r in gen]
        return r

    def dump(self) -> None:
        print("oids:")
        for i, oid in enumerate(self.repo.odb):
            print(f"oid[{i}]: {oid}")
        print("refs:")
        for i, ref in enumerate(self.references):
            print(f"ref[{i}]: {ref}")


if __name__ == "__main__":
    print(f"executing: {__file__}")
