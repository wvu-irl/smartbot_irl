# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...geometry_msgs.msg.pose import Pose
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class ArucoMarkers:
    header: Header = field(default_factory=Header)
    marker_ids: NDArray[numpy.int64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.int64))
    poses: list[Pose] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "ros2_aruco_interfaces/msg/ArucoMarkers"


__all__ = ["ArucoMarkers"]