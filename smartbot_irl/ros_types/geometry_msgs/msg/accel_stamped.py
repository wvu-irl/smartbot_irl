# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .accel import Accel
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class AccelStamped:
    header: Header = field(default_factory=Header)
    accel: Accel = field(default_factory=Accel)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/AccelStamped"


__all__ = ["AccelStamped"]