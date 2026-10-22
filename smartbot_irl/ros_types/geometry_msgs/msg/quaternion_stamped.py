# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .quaternion import Quaternion
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class QuaternionStamped:
    header: Header = field(default_factory=Header)
    quaternion: Quaternion = field(default_factory=Quaternion)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/QuaternionStamped"


__all__ = ["QuaternionStamped"]