from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

import numpy as np
from scipy.spatial.transform import Rotation as R

from smartbot_irl.ros_types.sensor_msgs.msg import Imu as RosImu
from smartbot_irl.utils import SmartLogger

from .base_type import BaseType

logger = SmartLogger(level=logging.INFO)  # Print statements, but better!


@dataclass
class Imu(BaseType):
    ros_type = 'sensor_msgs/Imu'

    # Orientation quaternion
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0
    qw: float = 1.0

    # Euler orientation
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0

    # Angular velocity
    wx: float = 0.0
    wy: float = 0.0
    wz: float = 0.0

    # Linear acceleration
    ax: float = 0.0
    ay: float = 0.0
    az: float = 0.0

    stamp_sec: int = 0
    stamp_nanosec: int = 0

    @classmethod
    def from_ros(cls, msg: RosImu):
        # ori = msg.orientation
        # ang = msg.angular_velocity
        # acc = msg.linear_acceleration

        q = np.array(
            [
                msg.orientation.x,
                msg.orientation.y,
                msg.orientation.z,
                msg.orientation.w,
            ]
        )

        roll, pitch, yaw = R.from_quat(q).as_euler(
            'xyz',
            degrees=False,
        )

        return cls(
            qx=q[0],
            qy=q[1],
            qz=q[2],
            qw=q[3],
            roll=roll,
            pitch=pitch,
            yaw=yaw,
            wx=msg.angular_velocity.x,
            wy=msg.angular_velocity.y,
            wz=msg.angular_velocity.z,
            ax=msg.linear_acceleration.x,
            ay=msg.linear_acceleration.y,
            az=msg.linear_acceleration.z,
            stamp_sec=msg.header.stamp.sec,
            stamp_nanosec=msg.header.stamp.nanosec,
        )

    def to_ros(self):
        return {
            'header': {
                'stamp': {'sec': self.stamp_sec, 'nanosec': self.stamp_nanosec},
            },
            'orientation': {
                'x': self.qx,
                'y': self.qy,
                'z': self.qz,
                'w': self.qw,
            },
            'angular_velocity': {
                'x': self.wx,
                'y': self.wy,
                'z': self.wz,
            },
            'linear_acceleration': {
                'x': self.ax,
                'y': self.ay,
                'z': self.az,
            },
        }
