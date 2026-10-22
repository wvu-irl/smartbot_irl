# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...std_msgs.msg.header import Header
from .joint_trajectory_point import JointTrajectoryPoint


@dataclass(slots=True)
class JointTrajectory:
    header: Header = field(default_factory=Header)
    joint_names: list[str] = field(default_factory=list)
    points: list[JointTrajectoryPoint] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "trajectory_msgs/msg/JointTrajectory"


__all__ = ["JointTrajectory"]