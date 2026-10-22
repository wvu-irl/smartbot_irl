# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .multi_array_layout import MultiArrayLayout


@dataclass(slots=True)
class Int32MultiArray:
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: NDArray[numpy.int32] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.int32))


    __msgtype__: ClassVar[str] = "std_msgs/msg/Int32MultiArray"


__all__ = ["Int32MultiArray"]