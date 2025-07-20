from attrs import define, field
from path import Path


@define(auto_attribs=True)
class RepoDB:
    path: Path = field(converter=Path)

    @property
    def git_obj_dir(self) -> Path:
        return self.path / ".git" / "objects"
