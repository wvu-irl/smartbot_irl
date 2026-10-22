# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import numpy
from numpy.typing import NDArray

from ...geometry_msgs.msg.polygon import Polygon


@dataclass(slots=True)
class SolidPrimitive:
    type: int = 0
    dimensions: NDArray[numpy.float64] = field(default_factory=lambda: numpy.empty(0, dtype=numpy.float64))
    polygon: Polygon = field(default_factory=Polygon)

    BOX: ClassVar[int] = 1
    SPHERE: ClassVar[int] = 2
    CYLINDER: ClassVar[int] = 3
    CONE: ClassVar[int] = 4
    PRISM: ClassVar[int] = 5
    BOX_X: ClassVar[int] = 0
    BOX_Y: ClassVar[int] = 1
    BOX_Z: ClassVar[int] = 2
    SPHERE_RADIUS: ClassVar[int] = 0
    CYLINDER_HEIGHT: ClassVar[int] = 0
    CYLINDER_RADIUS: ClassVar[int] = 1
    CONE_HEIGHT: ClassVar[int] = 0
    CONE_RADIUS: ClassVar[int] = 1
    PRISM_HEIGHT: ClassVar[int] = 0

    __msgtype__: ClassVar[str] = "shape_msgs/msg/SolidPrimitive"


__all__ = ["SolidPrimitive"]