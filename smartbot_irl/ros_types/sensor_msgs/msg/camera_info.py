# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .region_of_interest import RegionOfInterest
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class CameraInfo:
    header: Header = field(default_factory=Header)
    height: int = 0
    width: int = 0
    distortion_model: str = ""
    d: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    k: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(9, dtype=numpy.float64))
    r: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(9, dtype=numpy.float64))
    p: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(12, dtype=numpy.float64))
    binning_x: int = 0
    binning_y: int = 0
    roi: RegionOfInterest = field(default_factory=RegionOfInterest)


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/CameraInfo"


__all__ = ["CameraInfo"]