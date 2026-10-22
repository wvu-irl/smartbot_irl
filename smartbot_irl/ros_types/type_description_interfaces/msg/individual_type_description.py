# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .field import Field


@dataclass(slots=True)
class IndividualTypeDescription:
    type_name: str = ""
    fields: list[Field] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "type_description_interfaces/msg/IndividualTypeDescription"


__all__ = ["IndividualTypeDescription"]