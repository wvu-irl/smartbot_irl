# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .polygon_instance import PolygonInstance
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PolygonInstanceStamped:
    header: Header = field(default_factory=Header)
    polygon: PolygonInstance = field(default_factory=PolygonInstance)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/PolygonInstanceStamped"


__all__ = ["PolygonInstanceStamped"]