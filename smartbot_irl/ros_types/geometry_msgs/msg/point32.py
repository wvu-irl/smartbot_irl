# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar




@dataclass(slots=True)
class Point32:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Point32"


__all__ = ["Point32"]