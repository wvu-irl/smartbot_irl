# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray



@dataclass(slots=True)
class MeshTriangle:
    vertex_indices: NDArray[numpy.uint32] = field(default_factory=lambda: numpy.zeros(3, dtype=numpy.uint32))


    __msgtype__: ClassVar[str] = "shape_msgs/msg/MeshTriangle"


__all__ = ["MeshTriangle"]