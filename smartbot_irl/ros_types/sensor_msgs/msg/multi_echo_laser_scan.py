# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .laser_echo import LaserEcho
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class MultiEchoLaserScan:
    header: Header = field(default_factory=Header)
    angle_min: float = 0.0
    angle_max: float = 0.0
    angle_increment: float = 0.0
    time_increment: float = 0.0
    scan_time: float = 0.0
    range_min: float = 0.0
    range_max: float = 0.0
    ranges: list[LaserEcho] = field(default_factory=list)
    intensities: list[LaserEcho] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/MultiEchoLaserScan"


__all__ = ["MultiEchoLaserScan"]