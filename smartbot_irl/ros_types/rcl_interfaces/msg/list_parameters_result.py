# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class ListParametersResult:
    names: list[str] = field(default_factory=list)
    prefixes: list[str] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/ListParametersResult"


__all__ = ["ListParametersResult"]