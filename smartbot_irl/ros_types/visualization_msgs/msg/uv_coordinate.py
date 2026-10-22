# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class UVCoordinate:
    u: float = 0.0
    v: float = 0.0


    __msgtype__: ClassVar[str] = "visualization_msgs/msg/UVCoordinate"


__all__ = ["UVCoordinate"]