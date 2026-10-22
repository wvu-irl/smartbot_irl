# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class JointState:
    header: Header = field(default_factory=Header)
    name: list[str] = field(default_factory=list)
    position: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    velocity: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    effort: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/JointState"


__all__ = ["JointState"]