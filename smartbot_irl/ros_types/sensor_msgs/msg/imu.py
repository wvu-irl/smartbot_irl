# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...geometry_msgs.msg.quaternion import Quaternion
from ...geometry_msgs.msg.vector3 import Vector3
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Imu:
    header: Header = field(default_factory=Header)
    orientation: Quaternion = field(default_factory=Quaternion)
    orientation_covariance: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(9, dtype=numpy.float64))
    angular_velocity: Vector3 = field(default_factory=Vector3)
    angular_velocity_covariance: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(9, dtype=numpy.float64))
    linear_acceleration: Vector3 = field(default_factory=Vector3)
    linear_acceleration_covariance: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(9, dtype=numpy.float64))


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/Imu"


__all__ = ["Imu"]