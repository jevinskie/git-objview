from attrs import define, field
from path import Path


@define(auto_attribs=True)
class RepoDB:
    path: Path = field()
