# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .point32 import Point32


@dataclass(slots=True)
class Polygon:
    points: list[Point32] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Polygon"


__all__ = ["Polygon"]