# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.duration import Duration
from ...geometry_msgs.msg.transform import Transform
from ...geometry_msgs.msg.twist import Twist


@dataclass(slots=True)
class MultiDOFJointTrajectoryPoint:
    transforms: list[Transform] = field(default_factory=list)
    velocities: list[Twist] = field(default_factory=list)
    accelerations: list[Twist] = field(default_factory=list)
    time_from_start: Duration = field(default_factory=Duration)


    __msgtype__: ClassVar[str] = "trajectory_msgs/msg/MultiDOFJointTrajectoryPoint"


__all__ = ["MultiDOFJointTrajectoryPoint"]