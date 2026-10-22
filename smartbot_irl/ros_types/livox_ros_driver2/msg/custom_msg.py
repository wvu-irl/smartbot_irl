# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .custom_point import CustomPoint
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class CustomMsg:
    header: Header = field(default_factory=Header)
    timebase: int = 0
    point_num: int = 0
    lidar_id: int = 0
    rsvd: NDArray[numpy.uint8] = field(default_factory=lambda: numpy.zeros(3, dtype=numpy.uint8))
    points: list[CustomPoint] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "livox_ros_driver2/msg/CustomMsg"


__all__ = ["CustomMsg"]