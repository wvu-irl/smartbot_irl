# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .quaternion import Quaternion
from .vector3 import Vector3


@dataclass(slots=True)
class Transform:
    translation: Vector3 = field(default_factory=Vector3)
    rotation: Quaternion = field(default_factory=Quaternion)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Transform"


__all__ = ["Transform"]