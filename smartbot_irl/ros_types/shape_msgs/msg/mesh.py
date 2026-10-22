# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.point import Point
from .mesh_triangle import MeshTriangle


@dataclass(slots=True)
class Mesh:
    triangles: list[MeshTriangle] = field(default_factory=list)
    vertices: list[Point] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "shape_msgs/msg/Mesh"


__all__ = ["Mesh"]