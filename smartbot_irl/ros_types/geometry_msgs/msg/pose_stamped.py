# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .pose import Pose
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PoseStamped:
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/PoseStamped"


__all__ = ["PoseStamped"]