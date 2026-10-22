# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from .multi_array_layout import MultiArrayLayout


@dataclass(slots=True)
class Int16MultiArray:
    layout: MultiArrayLayout = field(default_factory=MultiArrayLayout)
    data: NDArray[numpy.int16] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.int16))


    __msgtype__: ClassVar[str] = "std_msgs/msg/Int16MultiArray"


__all__ = ["Int16MultiArray"]