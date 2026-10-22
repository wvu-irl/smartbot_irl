# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .polygon import Polygon


@dataclass(slots=True)
class PolygonInstance:
    polygon: Polygon = field(default_factory=Polygon)
    id: int = 0


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/PolygonInstance"


__all__ = ["PolygonInstance"]