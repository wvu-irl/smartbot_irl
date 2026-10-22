# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class TypeSource:
    type_name: str = ""
    encoding: str = ""
    raw_file_contents: str = ""


    __msgtype__: ClassVar[str] = "type_description_interfaces/msg/TypeSource"


__all__ = ["TypeSource"]