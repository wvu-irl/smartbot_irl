# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.point import Point
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class GridCells:
    header: Header = field(default_factory=Header)
    cell_width: float = 0.0
    cell_height: float = 0.0
    cells: list[Point] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "nav_msgs/msg/GridCells"


__all__ = ["GridCells"]