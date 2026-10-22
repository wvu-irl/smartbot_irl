from __future__ import annotations

from dataclasses import dataclass, field

from smartbot_irl.ros_types.sensor_msgs.msg import LaserScan as RosLaserScan

from .base_type import BaseType


@dataclass
class LaserScan(BaseType):
    """
    Simplified SmartBot-facing 2D laser scan.

    Attributes
    ----------
    ranges:
        Range readings in meters.

    angle_min:
        Start angle of the scan in radians.

    angle_max:
        End angle of the scan in radians.

    angle_increment:
        Angular distance between successive measurements in radians.
    """

    ranges: list[float] = field(default_factory=list)

    angle_min: float = 0.0
    angle_max: float = 0.0
    angle_increment: float = 0.0

    stamp_sec: int = 0
    stamp_nanosec: int = 0

    @classmethod
    def from_ros(cls, msg: RosLaserScan) -> LaserScan:
        return cls(
            ranges=list(msg.ranges),
            angle_min=msg.angle_min,
            angle_max=msg.angle_max,
            angle_increment=msg.angle_increment,
            stamp_sec=msg.header.stamp.sec,
            stamp_nanosec=msg.header.stamp.nanosec,
        )

    def to_ros(self) -> dict:
        return {
            'ranges': list(self.ranges),
            'angle_min': self.angle_min,
            'angle_max': self.angle_max,
            'angle_increment': self.angle_increment,
            'header': {
                'stamp': {
                    'sec': self.stamp_sec,
                    'nanosec': self.stamp_nanosec,
                },
            },
        }
