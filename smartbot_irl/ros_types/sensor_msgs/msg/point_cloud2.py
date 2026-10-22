# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .point_field import PointField
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PointCloud2:
    header: Header = field(default_factory=Header)
    height: int = 0
    width: int = 0
    fields: list[PointField] = field(default_factory=list)
    is_bigendian: bool = False
    point_step: int = 0
    row_step: int = 0
    data: NDArray[numpy.uint8] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.uint8))
    is_dense: bool = False


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/PointCloud2"


__all__ = ["PointCloud2"]