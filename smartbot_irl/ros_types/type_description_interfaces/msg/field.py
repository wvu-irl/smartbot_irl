# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .field_type import FieldType


@dataclass(slots=True)
class Field:
    name: str = ""
    type: FieldType = field(default_factory=FieldType)
    default_value: str = ""


    __msgtype__: ClassVar[str] = "type_description_interfaces/msg/Field"


__all__ = ["Field"]