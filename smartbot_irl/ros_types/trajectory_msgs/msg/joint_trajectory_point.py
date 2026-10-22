# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...builtin_interfaces.msg.duration import Duration


@dataclass(slots=True)
class JointTrajectoryPoint:
    positions: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    velocities: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    accelerations: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    effort: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    time_from_start: Duration = field(default_factory=Duration)


    __msgtype__: ClassVar[str] = "trajectory_msgs/msg/JointTrajectoryPoint"


__all__ = ["JointTrajectoryPoint"]