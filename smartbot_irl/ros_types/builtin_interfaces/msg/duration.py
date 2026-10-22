# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class Duration:
    sec: int = 0
    nanosec: int = 0


    __msgtype__: ClassVar[str] = "builtin_interfaces/msg/Duration"


__all__ = ["Duration"]