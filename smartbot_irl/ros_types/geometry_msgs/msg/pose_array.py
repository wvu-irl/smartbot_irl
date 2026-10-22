# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .pose import Pose
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PoseArray:
    header: Header = field(default_factory=Header)
    poses: list[Pose] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/PoseArray"


__all__ = ["PoseArray"]