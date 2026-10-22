# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .vector3 import Vector3


@dataclass(slots=True)
class Accel:
    linear: Vector3 = field(default_factory=Vector3)
    angular: Vector3 = field(default_factory=Vector3)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Accel"


__all__ = ["Accel"]