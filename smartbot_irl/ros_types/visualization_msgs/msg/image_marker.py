# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.duration import Duration
from ...geometry_msgs.msg.point import Point
from ...std_msgs.msg.color_rgba import ColorRGBA
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class ImageMarker:
    header: Header = field(default_factory=Header)
    ns: str = ""
    id: int = 0
    type: int = 0
    action: int = 0
    position: Point = field(default_factory=Point)
    scale: float = 0.0
    outline_color: ColorRGBA = field(default_factory=ColorRGBA)
    filled: int = 0
    fill_color: ColorRGBA = field(default_factory=ColorRGBA)
    lifetime: Duration = field(default_factory=Duration)
    points: list[Point] = field(default_factory=list)
    outline_colors: list[ColorRGBA] = field(default_factory=list)

    CIRCLE: ClassVar[int] = 0
    LINE_STRIP: ClassVar[int] = 1
    LINE_LIST: ClassVar[int] = 2
    POLYGON: ClassVar[int] = 3
    POINTS: ClassVar[int] = 4
    ADD: ClassVar[int] = 0
    REMOVE: ClassVar[int] = 1

    __msgtype__: ClassVar[str] = "visualization_msgs/msg/ImageMarker"


__all__ = ["ImageMarker"]