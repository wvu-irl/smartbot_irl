# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .twist import Twist


@dataclass(slots=True)
class TwistWithCovariance:
    twist: Twist = field(default_factory=Twist)
    covariance: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(36, dtype=numpy.float64))


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/TwistWithCovariance"


__all__ = ["TwistWithCovariance"]