# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .nav_sat_status import NavSatStatus
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class NavSatFix:
    header: Header = field(default_factory=Header)
    status: NavSatStatus = field(default_factory=NavSatStatus)
    latitude: float = 0.0
    longitude: float = 0.0
    altitude: float = 0.0
    position_covariance: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(9, dtype=numpy.float64))
    position_covariance_type: int = 0

    COVARIANCE_TYPE_UNKNOWN: ClassVar[int] = 0
    COVARIANCE_TYPE_APPROXIMATED: ClassVar[int] = 1
    COVARIANCE_TYPE_DIAGONAL_KNOWN: ClassVar[int] = 2
    COVARIANCE_TYPE_KNOWN: ClassVar[int] = 3

    __msgtype__: ClassVar[str] = "sensor_msgs/msg/NavSatFix"


__all__ = ["NavSatFix"]