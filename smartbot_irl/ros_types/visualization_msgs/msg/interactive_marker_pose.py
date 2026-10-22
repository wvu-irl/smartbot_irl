# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.pose import Pose
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class InteractiveMarkerPose:
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)
    name: str = ""


    __msgtype__: ClassVar[str] = "visualization_msgs/msg/InteractiveMarkerPose"


__all__ = ["InteractiveMarkerPose"]