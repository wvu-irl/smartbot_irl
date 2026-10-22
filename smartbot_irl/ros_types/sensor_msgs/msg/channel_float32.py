# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray



@dataclass(slots=True)
class ChannelFloat32:
    name: str = ""
    values: NDArray[numpy.float32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float32))


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/ChannelFloat32"


__all__ = ["ChannelFloat32"]