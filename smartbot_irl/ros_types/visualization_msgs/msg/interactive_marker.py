# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.pose import Pose
from ...std_msgs.msg.header import Header
from .interactive_marker_control import InteractiveMarkerControl
from .menu_entry import MenuEntry


@dataclass(slots=True)
class InteractiveMarker:
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)
    name: str = ""
    description: str = ""
    scale: float = 0.0
    menu_entries: list[MenuEntry] = field(default_factory=list)
    controls: list[InteractiveMarkerControl] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "visualization_msgs/msg/InteractiveMarker"


__all__ = ["InteractiveMarker"]