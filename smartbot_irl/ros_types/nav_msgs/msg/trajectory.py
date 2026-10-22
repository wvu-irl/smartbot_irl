# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .trajectory_point import TrajectoryPoint
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Trajectory:
    header: Header = field(default_factory=Header)
    points: list[TrajectoryPoint] = field(default_factory=list)


    __msgtype__: ClassVar[str] = "nav_msgs/msg/Trajectory"


__all__ = ["Trajectory"]