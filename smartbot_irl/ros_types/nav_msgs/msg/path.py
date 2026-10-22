# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.pose_stamped import PoseStamped
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Path:
    header: Header = field(default_factory=Header)
    poses: list[PoseStamped] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "nav_msgs/msg/Path"


__all__ = ["Path"]