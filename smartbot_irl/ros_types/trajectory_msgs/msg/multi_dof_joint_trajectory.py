# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...std_msgs.msg.header import Header
from .multi_dof_joint_trajectory_point import MultiDOFJointTrajectoryPoint


@dataclass(slots=True)
class MultiDOFJointTrajectory:
    header: Header = field(default_factory=Header)
    joint_names: list[str] = field(default_factory=list)
    points: list[MultiDOFJointTrajectoryPoint] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "trajectory_msgs/msg/MultiDOFJointTrajectory"


__all__ = ["MultiDOFJointTrajectory"]