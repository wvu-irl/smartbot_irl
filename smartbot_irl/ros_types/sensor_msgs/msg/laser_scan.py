# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class LaserScan:
    header: Header = field(default_factory=Header)
    angle_min: float = 0.0
    angle_max: float = 0.0
    angle_increment: float = 0.0
    time_increment: float = 0.0
    scan_time: float = 0.0
    range_min: float = 0.0
    range_max: float = 0.0
    ranges: NDArray[numpy.float32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float32))
    intensities: NDArray[numpy.float32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float32))


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/LaserScan"


__all__ = ["LaserScan"]