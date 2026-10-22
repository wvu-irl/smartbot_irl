# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class SetLoggerLevelsResult:
    successful: bool = False
    reason: str = ""


    __msgtype__: ClassVar[str] = "rcl_interfaces/msg/SetLoggerLevelsResult"


__all__ = ["SetLoggerLevelsResult"]