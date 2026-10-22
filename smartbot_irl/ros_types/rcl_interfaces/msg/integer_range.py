# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class IntegerRange:
    from_value: int = 0
    to_value: int = 0
    step: int = 0


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/IntegerRange"


__all__ = ["IntegerRange"]