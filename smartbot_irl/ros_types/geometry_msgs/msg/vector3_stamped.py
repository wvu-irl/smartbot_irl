# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .vector3 import Vector3
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Vector3Stamped:
    header: Header = field(default_factory=Header)
    vector: Vector3 = field(default_factory=Vector3)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/Vector3Stamped"


__all__ = ["Vector3Stamped"]