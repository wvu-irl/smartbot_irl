# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .accel import Accel


@dataclass(slots=True)
class AccelWithCovariance:
    accel: Accel = field(default_factory=Accel)
    covariance: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(36, dtype=numpy.float64))


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/AccelWithCovariance"


__all__ = ["AccelWithCovariance"]