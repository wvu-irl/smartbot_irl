# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.quaternion import Quaternion
from .marker import Marker


@dataclass(slots=True)
class InteractiveMarkerControl:
    name: str = ""
    orientation: Quaternion = field(default_factory=Quaternion)
    orientation_mode: int = 0
    interaction_mode: int = 0
    always_visible: bool = False
    markers: list[Marker] = field(default_factory=list)
    independent_marker_orientation: bool = False
    description: str = ""

    INHERIT: ClassVar[int] = 0
    FIXED: ClassVar[int] = 1
    VIEW_FACING: ClassVar[int] = 2
    NONE: ClassVar[int] = 0
    MENU: ClassVar[int] = 1
    BUTTON: ClassVar[int] = 2
    MOVE_AXIS: ClassVar[int] = 3
    MOVE_PLANE: ClassVar[int] = 4
    ROTATE_AXIS: ClassVar[int] = 5
    MOVE_ROTATE: ClassVar[int] = 6
    MOVE_3D: ClassVar[int] = 7
    ROTATE_3D: ClassVar[int] = 8
    MOVE_ROTATE_3D: ClassVar[int] = 9

    __msgtype__: ClassVar[str] = "visualization_msgs/msg/InteractiveMarkerControl"


__all__ = ["InteractiveMarkerControl"]