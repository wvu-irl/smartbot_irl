# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .vector3 import Vector3


@dataclass(slots=True)
class Inertia:
    m: float = 0.0
    com: Vector3 = field(default_factory=Vector3)
    ixx: float = 0.0
    ixy: float = 0.0
    ixz: float = 0.0
    iyy: float = 0.0
    iyz: float = 0.0
    izz: float = 0.0


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Inertia"


__all__ = ["Inertia"]