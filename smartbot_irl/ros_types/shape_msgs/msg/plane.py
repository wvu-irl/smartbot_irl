# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray



@dataclass(slots=True)
class Plane:
    coef: NDArray[numpy.float64] = field(default_factory=lambda: numpy.zeros(4, dtype=numpy.float64))


    __msgtype__: ClassVar[str] = "shape_msgs/msg/Plane"


__all__ = ["Plane"]