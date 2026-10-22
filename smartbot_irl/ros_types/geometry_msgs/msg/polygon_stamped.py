# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .polygon import Polygon
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PolygonStamped:
    header: Header = field(default_factory=Header)
    polygon: Polygon = field(default_factory=Polygon)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/PolygonStamped"


__all__ = ["PolygonStamped"]