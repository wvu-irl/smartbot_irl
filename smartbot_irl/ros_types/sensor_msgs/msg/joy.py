# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Joy:
    header: Header = field(default_factory=Header)
    axes: NDArray[numpy.float32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float32))
    buttons: NDArray[numpy.int32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.int32))


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/Joy"


__all__ = ["Joy"]