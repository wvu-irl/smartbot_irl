# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .individual_type_description import IndividualTypeDescription


@dataclass(slots=True)
class TypeDescription:
    type_description: IndividualTypeDescription = field(default_factory=IndividualTypeDescription)
    referenced_type_descriptions: list[IndividualTypeDescription] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "type_description_interfaces/msg/TypeDescription"


__all__ = ["TypeDescription"]