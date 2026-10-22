# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .floating_point_range import FloatingPointRange
from .integer_range import IntegerRange


@dataclass(slots=True)
class ParameterDescriptor:
    name: str = ""
    type: int = 0
    description: str = ""
    additional_constraints: str = ""
    read_only: bool = False
    dynamic_typing: bool = False
    floating_point_range: list[FloatingPointRange] = field(default_factory=list)
    integer_range: list[IntegerRange] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/ParameterDescriptor"


__all__ = ["ParameterDescriptor"]