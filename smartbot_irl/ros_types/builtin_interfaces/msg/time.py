# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class Time:
    sec: int = 0
    nanosec: int = 0


    __msgtype__: ClassVar[str] = "builtin_interfaces/msg/Time"


__all__ = ["Time"]