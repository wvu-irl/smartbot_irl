# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.time import Time
from ...geometry_msgs.msg.pose import Pose


@dataclass(slots=True)
class MapMetaData:
    map_load_time: Time = field(default_factory=Time)
    resolution: float = 0.0
    width: int = 0
    height: int = 0
    origin: Pose = field(default_factory=Pose)


    __msgtype__: ClassVar[str] = "nav_msgs/msg/MapMetaData"


__all__ = ["MapMetaData"]