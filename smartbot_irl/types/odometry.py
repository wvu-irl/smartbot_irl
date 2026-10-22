from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial.transform import Rotation as R

from smartbot_irl.ros_types.nav_msgs.msg import Odometry as RosOdometry

from .base_type import BaseType


@dataclass
class Odometry(BaseType):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0
    qw: float = 1.0

    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0

    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0

    wx: float = 0.0
    wy: float = 0.0
    wz: float = 0.0

    stamp_sec: int = 0
    stamp_nanosec: int = 0

    @classmethod
    def from_ros(cls, msg: RosOdometry) -> Odometry:
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation

        linear = msg.twist.twist.linear
        angular = msg.twist.twist.angular

        q = np.array(
            [
                orientation.x,
                orientation.y,
                orientation.z,
                orientation.w,
            ]
        )

        roll, pitch, yaw = R.from_quat(q).as_euler(
            'xyz',
            degrees=False,
        )

        return cls(
            x=position.x,
            y=position.y,
            z=position.z,
            qx=orientation.x,
            qy=orientation.y,
            qz=orientation.z,
            qw=orientation.w,
            roll=roll,
            pitch=pitch,
            yaw=yaw,
            vx=linear.x,
            vy=linear.y,
            vz=linear.z,
            wx=angular.x,
            wy=angular.y,
            wz=angular.z,
            stamp_sec=msg.header.stamp.sec,
            stamp_nanosec=msg.header.stamp.nanosec,
        )

    def to_ros(self) -> dict:
        return {
            'pose': {
                'pose': {
                    'position': {
                        'x': self.x,
                        'y': self.y,
                        'z': self.z,
                    },
                    'orientation': {
                        'x': self.qx,
                        'y': self.qy,
                        'z': self.qz,
                        'w': self.qw,
                    },
                },
            },
            'twist': {
                'twist': {
                    'linear': {
                        'x': self.vx,
                        'y': self.vy,
                        'z': self.vz,
                    },
                    'angular': {
                        'x': self.wx,
                        'y': self.wy,
                        'z': self.wz,
                    },
                },
            },
            'header': {
                'stamp': {
                    'sec': self.stamp_sec,
                    'nanosec': self.stamp_nanosec,
                },
            },
        }
