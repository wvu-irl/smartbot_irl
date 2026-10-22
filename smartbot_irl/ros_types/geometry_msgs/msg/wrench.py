# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .vector3 import Vector3


@dataclass(slots=True)
class Wrench:
    force: Vector3 = field(default_factory=Vector3)
    torque: Vector3 = field(default_factory=Vector3)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Wrench"


__all__ = ["Wrench"]