# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .point import Point
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PointStamped:
    header: Header = field(default_factory=Header)
    point: Point = field(default_factory=Point)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/PointStamped"


__all__ = ["PointStamped"]