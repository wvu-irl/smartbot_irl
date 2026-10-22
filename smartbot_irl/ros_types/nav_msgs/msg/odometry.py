# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...geometry_msgs.msg.pose_with_covariance import PoseWithCovariance
from ...geometry_msgs.msg.twist_with_covariance import TwistWithCovariance
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class Odometry:
    header: Header = field(default_factory=Header)
    child_frame_id: str = ""
    pose: PoseWithCovariance = field(default_factory=PoseWithCovariance)
    twist: TwistWithCovariance = field(default_factory=TwistWithCovariance)


    __msgtype__: ClassVar[str] = "nav_msgs/msg/Odometry"


__all__ = ["Odometry"]