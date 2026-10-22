# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .map_meta_data import MapMetaData
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class OccupancyGrid:
    header: Header = field(default_factory=Header)
    info: MapMetaData = field(default_factory=MapMetaData)
    data: NDArray[numpy.int8] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.int8))


    __msgtype__: ClassVar[str] = "nav_msgs/msg/OccupancyGrid"


__all__ = ["OccupancyGrid"]