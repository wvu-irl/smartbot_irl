from __future__ import annotations

from dataclasses import dataclass, field

from smartbot_irl.ros_types.geometry_msgs.msg import PoseArray as RosPoseArray

from .base_type import BaseType
from .pose import Pose


@dataclass
class PoseArray(BaseType):
    poses: list[Pose] = field(default_factory=list)
    stamp_sec: int = 0
    stamp_nanosec: int = 0

    @classmethod
    def from_ros(cls, msg: RosPoseArray) -> PoseArray:
        return cls(
            poses=[Pose.from_ros(p) for p in msg.poses],
            stamp_sec=msg.header.stamp.sec,
            stamp_nanosec=msg.header.stamp.nanosec,
        )

    def to_ros(self) -> dict:
        return {
            'poses': [pose.to_ros() for pose in self.poses],
            'header': {
                'stamp': {
                    'sec': self.stamp_sec,
                    'nanosec': self.stamp_nanosec,
                },
            },
        }
