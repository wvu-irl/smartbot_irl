# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .point import Point
from .quaternion import Quaternion


@dataclass(slots=True)
class Pose:
    position: Point = field(default_factory=Point)
    orientation: Quaternion = field(default_factory=Quaternion)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Pose"


__all__ = ["Pose"]