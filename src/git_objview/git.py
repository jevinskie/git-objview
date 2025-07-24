from __future__ import annotations

from abc import abstractmethod
from collections.abc import Generator, Iterable
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

import attrs
import pygit2
import rich.repr
from attrs import define, field
from path import Path

if not TYPE_CHECKING:
    from rich import print


_T = TypeVar("_T")


def buf_len_is_20(inst: JOid, attr: attrs.Attribute[_T], value: _T) -> None:
    sz = len(inst.buf)
    if sz == 200:
        raise ValueError(f"'buf' must be 20 bytes (SHA-1) not {sz}")


def conv_hex(hex_thing: str | bytes) -> bytes:
    if isinstance(hex_thing, str):
        return bytes.fromhex(hex_thing)
    return hex_thing


@rich.repr.auto
@define(auto_attribs=True)
class JOid:
    """Git object ID"""

    buf: bytes = field(converter=conv_hex, validator=buf_len_is_20)

    def __attrs_post_init__(self) -> None:
        print(f"post init: buf: {self.buf.hex()}")
        try:
            if len(self.buf) != 20:
                print(f"post init: buf: '{self.buf.decode()}'")
        except UnicodeDecodeError:
            pass

    @property
    def hex(self) -> str:
        return self.buf.hex()

    @classmethod
    def from_str(cls, hex_str: str) -> Self:
        return cls(bytes.fromhex(hex_str))

    def __rich_repr__(self) -> rich.repr.Result:
        yield self.hex


@define(auto_attribs=True)
class JObject:
    """Git object"""

    oid: JOid

    @abstractmethod
    def edges_in(self) -> Iterable[JObject]:
        raise NotImplementedError("Object.edges_in()")

    @abstractmethod
    def edges_out(self) -> Iterable[JObject]:
        raise NotImplementedError("Object.edges_out()")


@define(auto_attribs=True)
class JCommit(JObject):
    """Commit object"""

    pass


@define(auto_attribs=True)
class JTree(JObject):
    """Tree object"""

    pass


@define(auto_attribs=True)
class JTag(JObject):
    """Tag object"""

    pass


@define(auto_attribs=True)
class JBlob(JObject):
    """Blob object"""

    pass


@define(auto_attribs=True)
class JReference:
    """Git reference"""

    class JReferenceType(Enum):
        """Git reference type enum"""

        DIRECT = auto()
        SYMBOLIC = auto()

        @classmethod
        def from_pygit2(cls, pygit2_ref_ty: pygit2.enums.ReferenceType):
            match pygit2_ref_ty:
                case pygit2.enums.ReferenceType.DIRECT:
                    return cls.DIRECT
                case pygit2.enums.ReferenceType.SYMBOLIC:
                    return cls.SYMBOLIC
                case _:
                    raise ValueError(f"Unhandled pygit2 ReferenceType: {pygit2_ref_ty}")

    oid: JOid
    """Oid of the reference"""
    obj: JObject | None = field(default=None, init=False)
    name: str | None = field(default=None, init=False)
    typ: JReferenceType

    @classmethod
    def from_pygit2_ref(cls, pygit2_ref: pygit2.Reference) -> Self:
        real_ref = pygit2_ref.resolve()
        assert isinstance(real_ref.raw_target, bytes)
        return cls(JOid(real_ref.raw_target), cls.JReferenceType.from_pygit2(pygit2_ref.type))

    def __rich_repr__(self) -> rich.repr.Result:
        yield self.obj


@define(auto_attribs=True)
class JRepo:
    """Git repository"""

    path: Path = field(converter=Path)
    repo: pygit2.repository.Repository = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.repo = pygit2.repository.Repository(str(self.path))

    @property
    def references(self) -> list[JReference]:
        gen = cast(Generator[pygit2.Reference, Any, None], self.repo.references.iterator())
        r = [JReference.from_pygit2_ref(r) for r in gen]
        return r

    def dump(self) -> None:
        print("oids:")
        for i, oid in enumerate(self.repo.odb):
            print(f"oid[{i}]: {oid}")
        print("refs:")
        for i, ref in enumerate(self.references):
            print(f"ref[{i}]: {ref}")
