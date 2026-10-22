# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class FloatingPointRange:
    from_value: float = 0.0
    to_value: float = 0.0
    step: float = 0.0


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/FloatingPointRange"


__all__ = ["FloatingPointRange"]