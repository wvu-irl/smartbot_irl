from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

import numpy as np
from scipy.spatial.transform import Rotation as R

from smartbot_irl.utils import SmartLogger

from .base_type import BaseType

logger = SmartLogger(level=logging.INFO)  # Print statements, but better!


@dataclass
class Pose(BaseType):
    """
    Generic pose with position, quaternion orientation,
    and roll pitch yaw angles.

    Maps to ROS2 message``geometry_msgs/Pose``. Has RPY angles for convenience.

    Attributes
    -------
        x (float): Position along the X-axis in meters.
        y (float): Position along the Y-axis in meters.
        z (float): Position along the Z-axis in meters.
        qx (float): Quaternion X component.
        qy (float): Quaternion Y component.
        qz (float): Quaternion Z component.
        qw (float): Quaternion W component.
        roll (float): Roll angle in radians.
        pitch (float): Pitch angle in radians.
        yaw (float): Yaw angle in radians.
    """

    ros_type = 'geometry_msgs/Pose'

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
    stamp_sec: int = 0
    stamp_nanosec: int = 0

    @classmethod
    def from_ros(cls, msg: dict) -> Pose:
        """
        Create a ``Pose`` from a ROS ``geometry_msgs/Pose`` msg.

        The method extracts the ``position`` and ``orientation`` fields,
        converts the quaternion to roll–pitch–yaw using
        ``scipy.spatial.transform.Rotation``, and returns a populated ``Pose``.

        Parameters
        ----------
            msg (dict): Dict corresponding to ros2 ``geometry_msgs/Pose``
            message with``position`` and ``orientation`` keys

        Returns
        -------
            Pose: Parsed pose instance.
        """
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
            x=msg.position.x,
            y=msg.position.y,
            z=msg.position.z,
            qx=q[0],
            qy=q[1],
            qz=q[2],
            qw=q[3],
            roll=roll,
            pitch=pitch,
            yaw=yaw,
        )

    def to_ros(self) -> dict:
        return {
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
        }
