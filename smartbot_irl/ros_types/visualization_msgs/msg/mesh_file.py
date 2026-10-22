# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray



@dataclass(slots=True)
class MeshFile:
    filename: str = ""
    data: NDArray[numpy.uint8] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.uint8))


    __msgtype__: ClassVar[str] = "visualization_msgs/msg/MeshFile"


__all__ = ["MeshFile"]