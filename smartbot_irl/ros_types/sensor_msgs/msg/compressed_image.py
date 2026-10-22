# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class CompressedImage:
    header: Header = field(default_factory=Header)
    format: str = ""
    data: NDArray[numpy.uint8] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.uint8))


    __msgtype__: ClassVar[str] = "sensor_msgs/msg/CompressedImage"


__all__ = ["CompressedImage"]