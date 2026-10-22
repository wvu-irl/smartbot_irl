# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.point import Point
from ...geometry_msgs.msg.pose import Pose
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class InteractiveMarkerFeedback:
    header: Header = field(default_factory=Header)
    client_id: str = ""
    marker_name: str = ""
    control_name: str = ""
    event_type: int = 0
    pose: Pose = field(default_factory=Pose)
    menu_entry_id: int = 0
    mouse_point: Point = field(default_factory=Point)
    mouse_point_valid: bool = False

    KEEP_ALIVE: ClassVar[int] = 0
    POSE_UPDATE: ClassVar[int] = 1
    MENU_SELECT: ClassVar[int] = 2
    BUTTON_CLICK: ClassVar[int] = 3
    MOUSE_DOWN: ClassVar[int] = 4
    MOUSE_UP: ClassVar[int] = 5

    __msgtype__: ClassVar[str] = "visualization_msgs/msg/InteractiveMarkerFeedback"


__all__ = ["InteractiveMarkerFeedback"]