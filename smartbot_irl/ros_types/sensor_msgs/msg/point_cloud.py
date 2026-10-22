# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.point32 import Point32
from .channel_float32 import ChannelFloat32
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PointCloud:
    header: Header = field(default_factory=Header)
    points: list[Point32] = field(default_factory=list)
    channels: list[ChannelFloat32] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/PointCloud"


__all__ = ["PointCloud"]