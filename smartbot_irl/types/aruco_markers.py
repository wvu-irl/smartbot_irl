from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..ros_types.ros2_aruco_interfaces.msg import ArucoMarkers as RosArucoMarkers
from .base_type import BaseType
from .pose import Pose


@dataclass
class ArucoMarkers(BaseType):
    poses: list[Pose] = field(default_factory=list)
    marker_ids: list[int] = field(default_factory=list)

    stamp_sec: int = 0
    stamp_nanosec: int = 0

    # On second thought this is stupid.
    # # Adjustable thingies:
    # mapping_spec: SensorSpec = SensorSpec()

    # def setup(self, ros_topic_name: str, ros_type: type[Any], timeout: float):
    #     """This has to be to set before it can be used to register pub/sub"""
    #     self.mapping_spec.ros_type = ros_type
    #     self.mapping_spec.ros_topic = ros_topic_name
    #     self.mapping_spec.timeout = timeout
    #     self.mapping_spec.type = type(self)  # Uh.

    @classmethod
    def from_ros(cls, msg: RosArucoMarkers) -> ArucoMarkers:
        return cls(
            poses=[Pose.from_ros(msg=p) for p in msg.poses],
            marker_ids=list(msg.marker_ids),
            stamp_sec=msg.header.stamp.sec,
            stamp_nanosec=msg.header.stamp.nanosec,
        )

    def to_ros(self) -> dict[str, Any]:
        return {
            "poses": [pose.to_ros() for pose in self.poses],
            "marker_ids": list(self.marker_ids),
            "header": {
                "stamp": {
                    "sec": self.stamp_sec,
                    "nanosec": self.stamp_nanosec,
                },
            },
        }
