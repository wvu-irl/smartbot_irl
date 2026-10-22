# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.accel import Accel
from ...geometry_msgs.msg.pose import Pose
from ...geometry_msgs.msg.twist import Twist
from ...geometry_msgs.msg.wrench import Wrench
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class TrajectoryPoint:
    header: Header = field(default_factory=Header)
    pose: Pose = field(default_factory=Pose)
    velocity: Twist = field(default_factory=Twist)
    acceleration: Accel = field(default_factory=Accel)
    effort: Wrench = field(default_factory=Wrench)


    __msgtype__: ClassVar[str] = "nav_msgs/msg/TrajectoryPoint"


__all__ = ["TrajectoryPoint"]