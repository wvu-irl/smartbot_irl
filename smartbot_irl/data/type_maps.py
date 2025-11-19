"""Data types for SmartBot."""

# smartbot_irl/data/type_maps.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Dict
from scipy.spatial.transform import Rotation as R
import numpy as np

import inspect


def _hide_signature(cls):
    cls.__signature__ = inspect.Signature()
    return cls


class Pose:
    """
    Generic pose with position, quaternion orientation, and roll/pitch/yaw angles.

    Attributes
    ----------
    x : float, default=0
        Position along the X-axis in meters.
    y : float, default=0
        Position along the Y-axis in meters.
    z : float, default=0
        Position along the Z-axis in meters.
    qx : float, default=0
        Quaternion X component.
    qy : float, default=0.0
        Quaternion Y component.
    qz : float, default=0.0
        Quaternion Z component.
    qw : float, default=1.0
        Quaternion W component.
    roll : float, default=0.0
        Roll angle in radians.
    pitch : float, default=0.0
        Pitch angle in radians.
    yaw : float, default=0.0
        Yaw angle in radians.
    """

    _ros_type = 'geometry_msgs/Pose'

    def __init__(
        self,
        x=0.0,
        y=0.0,
        z=0.0,
        qx=0.0,
        qy=0.0,
        qz=0.0,
        qw=1.0,
        roll=0.0,
        pitch=0.0,
        yaw=0.0,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.qx = qx
        self.qy = qy
        self.qz = qz
        self.qw = qw
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    @classmethod
    def _from_ros(cls, msg: dict) -> Pose:
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
        pos = msg.get('position', {})
        ori = msg.get('orientation', {})
        q = np.array(
            [
                ori.get('x', 0.0),
                ori.get('y', 0.0),
                ori.get('z', 0.0),
                ori.get('w', 1.0),
            ]
        )
        roll, pitch, yaw = R.from_quat(q).as_euler('xyz', degrees=False)
        return cls(
            x=pos.get('x', 0.0),
            y=pos.get('y', 0.0),
            z=pos.get('z', 0.0),
            qx=q[0],
            qy=q[1],
            qz=q[2],
            qw=q[3],
            roll=roll,
            pitch=pitch,
            yaw=yaw,
        )

    # TODO convert RPY back to quat?
    def _to_ros(self) -> dict[str, dict[str, float]]:
        """
        Create a ``geometry_msgs/Pose`` from a ROS ``Pose`` msg.

        The method extracts the ``position`` and ``orientation`` fields, then
        builds a dict matching the ROS2 ``geometry_msgs/Pose`` message
        structure.

        Returns:
            dict[str, dict[str, float]]: Dict mirroring ROS2
            ``geometry_msgs/Pose`` message structure.

        Example:
            >>> p = Pose(x=1.0, y=2.0, yaw=3.14)
            >>> ros = p._to_ros()
        """
        return {
            'position': {'x': self.x, 'y': self.y, 'z': self.z},
            'orientation': {'x': self.qx, 'y': self.qy, 'z': self.qz, 'w': self.qw},
        }


class Odometry:
    """
    Robot odometry containing pose, orientation, and twist information.

    Mirrors the ROS2 message type ``nav_msgs/Odometry`` and provides helpers
    for converting to and from the ROS dictionary representation used by
    lightweight ROS interfaces. The pose contains position and orientation
    (as both a quaternion and roll–pitch–yaw), and the twist contains the
    linear and angular velocities.

    Attributes
    ----------
    x : float
        Position along the X-axis in meters.
    y : float
        Position along the Y-axis in meters.
    z : float
        Position along the Z-axis in meters.

    qx : float
        Quaternion X component.
    qy : float
        Quaternion Y component.
    qz : float
        Quaternion Z component.
    qw : float
        Quaternion W component.

    roll : float
        Roll angle in radians.
    pitch : float
        Pitch angle in radians.
    yaw : float
        Yaw angle in radians.

    vx : float
        Linear X-velocity in meters per second.
    vy : float
        Linear Y-velocity in meters per second.
    vz : float
        Linear Z-velocity in meters per second.

    wx : float
        Angular X-velocity in radians per second.
    wy : float
        Angular Y-velocity in radians per second.
    wz : float
        Angular Z-velocity in radians per second.
    """

    _ros_type = 'nav_msgs/Odometry'

    def __init__(
        self,
        x=0.0,
        y=0.0,
        z=0.0,
        qx=0.0,
        qy=0.0,
        qz=0.0,
        qw=1.0,
        roll=0.0,
        pitch=0.0,
        yaw=0.0,
        vx=0.0,
        vy=0.0,
        vz=0.0,
        wx=0.0,
        wy=0.0,
        wz=0.0,
    ) -> None:
        # Position
        self.x = x
        self.y = y
        self.z = z

        # Orientation quaternion
        self.qx = qx
        self.qy = qy
        self.qz = qz
        self.qw = qw

        # Euler
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

        # Linear velocities
        self.vx = vx
        self.vy = vy
        self.vz = vz

        # Angular velocities
        self.wx = wx
        self.wy = wy
        self.wz = wz

    @classmethod
    def _from_ros(cls, msg: dict) -> 'Odometry':
        """
        Create an ``Odometry`` instance from a ROS ``nav_msgs/Odometry`` dictionary.

        Parameters
        ----------
        msg : dict
            ROS-style dictionary containing nested ``pose`` and ``twist`` fields.

        Returns
        -------
        Odometry
            Parsed odometry instance populated with pose and twist values.
        """

        pose = msg.get('pose', {}).get('pose', {})
        pos = pose.get('position', {})
        ori = pose.get('orientation', {})

        q = np.array(
            [
                ori.get('x', 0.0),
                ori.get('y', 0.0),
                ori.get('z', 0.0),
                ori.get('w', 1.0),
            ]
        )

        roll, pitch, yaw = R.from_quat(q).as_euler('xyz', degrees=False)

        twist = msg.get('twist', {}).get('twist', {})
        lin = twist.get('linear', {})
        ang = twist.get('angular', {})

        return cls(
            x=pos.get('x', 0.0),
            y=pos.get('y', 0.0),
            z=pos.get('z', 0.0),
            qx=q[0],
            qy=q[1],
            qz=q[2],
            qw=q[3],
            roll=roll,
            pitch=pitch,
            yaw=yaw,
            vx=lin.get('x', 0.0),
            vy=lin.get('y', 0.0),
            vz=lin.get('z', 0.0),
            wx=ang.get('x', 0.0),
            wy=ang.get('y', 0.0),
            wz=ang.get('z', 0.0),
        )

    def _to_ros(self):
        """
        Convert this odometry instance back into a ROS-style dictionary.

        Returns
        -------
        dict
            Dictionary matching the ``nav_msgs/Odometry`` message structure.
        """

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
                }
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
                }
            },
        }


class PoseArray:
    """
    Array of ``Pose`` objects, mirroring the ROS message
    ``geometry_msgs/PoseArray``.

    Attributes
    ----------
    poses : list of Pose
        List of pose elements contained in the array.
    """

    _ros_type = 'geometry_msgs/PoseArray'

    def __init__(self, poses=None) -> None:
        self.poses = poses if poses is not None else []

    @classmethod
    def _from_ros(cls, msg: dict) -> 'PoseArray':
        """
        Create a ``PoseArray`` from a ROS-style dictionary.

        Parameters
        ----------
        msg : dict
            Dictionary with a ``poses`` key containing a list of pose dicts.

        Returns
        -------
        PoseArray
            Parsed pose array containing ``Pose`` objects.
        """
        pose_dicts = msg.get('poses', [])
        poses = [Pose._from_ros(p) for p in pose_dicts]
        return cls(poses=poses)

    def _to_ros(self) -> dict:
        """
        Convert this ``PoseArray`` to a ROS-style dictionary.

        Returns
        -------
        dict
            Dictionary with a ``poses`` key containing ROS pose dicts.
        """
        return {'poses': [p._to_ros() for p in self.poses]}


class ArucoMarkers:
    """
    Collection of detected ArUco marker poses and their IDs.

    Mirrors the ROS message type ``ros2_aruco_interfaces/ArucoMarkers``.

    Attributes
    ----------
    poses : list of Pose
        List of detected marker poses.
    marker_ids : list of int
        Integer IDs corresponding to each detected marker.
    """

    _ros_type = 'ros2_aruco_interfaces/ArucoMarkers'

    def __init__(
        self,
        poses: list[Pose] | None = None,
        marker_ids: list[int] | None = None,
    ) -> None:
        self.poses = poses if poses is not None else []
        self.marker_ids = marker_ids if marker_ids is not None else []

    @classmethod
    def _from_ros(cls, msg: dict) -> 'ArucoMarkers':
        """
        Create an ``ArucoMarkers`` instance from a ROS-style dictionary.

        Parameters
        ----------
        msg : dict
            Dictionary containing ``poses`` and ``marker_ids`` keys.

        Returns
        -------
        ArucoMarkers
            Parsed marker set with poses and IDs.
        """
        pose_dicts = msg.get('poses', [])
        poses = [Pose._from_ros(p) for p in pose_dicts]

        ids = list(msg.get('marker_ids', []))

        return cls(poses=poses, marker_ids=ids)

    def _to_ros(self) -> dict:
        """
        Convert this ``ArucoMarkers`` object into a ROS-style dictionary.

        Returns
        -------
        dict
            Dictionary containing ``poses`` and ``marker_ids``.
        """
        return {
            'poses': [p._to_ros() for p in self.poses],
            'marker_ids': list(self.marker_ids),
        }


class LaserScan:
    """
    Represents a 2D planar laser scan message.

    Mirrors the ROS message type ``sensor_msgs/LaserScan`` and provides
    helpers for converting to and from the ROS-style dictionary form.

    Attributes
    ----------
    ranges : list of float
        Range readings from the laser in meters. Each value corresponds to a beam.
    angle_min : float
        Start angle of the scan, in radians (usually negative).
    angle_max : float
        End angle of the scan, in radians.
    angle_increment : float
        Angular distance between successive measurements, in radians.
    """

    _ros_type = 'sensor_msgs/LaserScan'

    def __init__(
        self,
        ranges=None,
        angle_min=0.0,
        angle_max=0.0,
        angle_increment=0.0,
    ) -> None:
        self.ranges = ranges if ranges is not None else []
        self.angle_min = angle_min
        self.angle_max = angle_max
        self.angle_increment = angle_increment

    @classmethod
    def _from_ros(cls, msg: dict) -> 'LaserScan':
        """
        Create a ``LaserScan`` from a ROS-style dictionary.

        Parameters
        ----------
        msg : dict
            Dictionary with keys matching ``sensor_msgs/LaserScan`` fields.

        Returns
        -------
        LaserScan
            Parsed scan instance.
        """
        return cls(
            ranges=msg.get('ranges', []),
            angle_min=msg.get('angle_min', 0.0),
            angle_max=msg.get('angle_max', 0.0),
            angle_increment=msg.get('angle_increment', 0.0),
        )

    def _to_ros(self) -> dict:
        """
        Convert this scan into a ROS-style dictionary.

        Returns
        -------
        dict
            Dictionary with ``ranges`` and angle metadata.
        """
        return {
            'ranges': self.ranges,
            'angle_min': self.angle_min,
            'angle_max': self.angle_max,
            'angle_increment': self.angle_increment,
        }


class JointState:
    """
    Represents a robot joint state message.

    Mirrors the ROS message type ``sensor_msgs/JointState`` and provides
    conversion helpers to and from the ROS-style dictionary format.

    Attributes
    ----------
    names : list of str
        Joint names in order corresponding to the numerical arrays.
    positions : list of float
        Joint positions (typically radians or meters).
    velocities : list of float
        Joint velocities (same order as positions).
    """

    _ros_type = 'sensor_msgs/JointState'

    def __init__(
        self,
        names=None,
        positions=None,
        velocities=None,
    ) -> None:
        self.names = names if names is not None else []
        self.positions = positions if positions is not None else []
        self.velocities = velocities if velocities is not None else []

    @classmethod
    def _from_ros(cls, msg: dict) -> 'JointState':
        """
        Create a ``JointState`` from a ROS-style dictionary.

        Parameters
        ----------
        msg : dict
            Dictionary with keys ``name``, ``position``, and ``velocity``.

        Returns
        -------
        JointState
            Parsed joint state instance.
        """
        return cls(
            names=msg.get('name', []),
            positions=msg.get('position', []),
            velocities=msg.get('velocity', []),
        )

    def _to_ros(self) -> dict:
        """
        Convert this joint state into a ROS-style dictionary.

        Returns
        -------
        dict
            Dictionary with ``name``, ``position``, and ``velocity`` fields.
        """
        return {
            'name': self.names,
            'position': self.positions,
            'velocity': self.velocities,
        }


class IMU:
    """
    Represents an IMU message containing orientation, angular velocity,
    and linear acceleration.

    Mirrors the ROS message type ``sensor_msgs/Imu`` and provides helpers
    for converting to and from the ROS-style dictionary representation.

    Attributes
    ----------
    qx : float
        Quaternion X component.
    qy : float
        Quaternion Y component.
    qz : float
        Quaternion Z component.
    qw : float
        Quaternion W component.

    roll : float
        Roll angle in radians.
    pitch : float
        Pitch angle in radians.
    yaw : float
        Yaw angle in radians.

    wx : float
        Angular velocity around X-axis in rad/s.
    wy : float
        Angular velocity around Y-axis in rad/s.
    wz : float
        Angular velocity around Z-axis in rad/s.

    ax : float
        Linear acceleration in X in m/s^2.
    ay : float
        Linear acceleration in Y in m/s^2.
    az : float
        Linear acceleration in Z in m/s^2.
    """

    _ros_type = 'sensor_msgs/Imu'

    def __init__(
        self,
        qx=0.0,
        qy=0.0,
        qz=0.0,
        qw=1.0,
        roll=0.0,
        pitch=0.0,
        yaw=0.0,
        wx=0.0,
        wy=0.0,
        wz=0.0,
        ax=0.0,
        ay=0.0,
        az=0.0,
    ) -> None:
        self.qx = qx
        self.qy = qy
        self.qz = qz
        self.qw = qw

        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

        self.wx = wx
        self.wy = wy
        self.wz = wz

        self.ax = ax
        self.ay = ay
        self.az = az

    @classmethod
    def _from_ros(cls, msg: dict) -> 'IMU':
        """
        Create an ``IMU`` instance from a ROS-style dictionary.

        Parameters
        ----------
        msg : dict
            Dictionary with ``orientation``, ``angular_velocity``,
            and ``linear_acceleration`` fields.

        Returns
        -------
        IMU
            Parsed IMU instance.
        """
        ori = msg.get('orientation', {})
        ang = msg.get('angular_velocity', {})
        acc = msg.get('linear_acceleration', {})

        q = np.array(
            [
                ori.get('x', 0.0),
                ori.get('y', 0.0),
                ori.get('z', 0.0),
                ori.get('w', 1.0),
            ]
        )

        roll, pitch, yaw = R.from_quat(q).as_euler('xyz', degrees=False)

        return cls(
            qx=q[0],
            qy=q[1],
            qz=q[2],
            qw=q[3],
            roll=roll,
            pitch=pitch,
            yaw=yaw,
            wx=ang.get('x', 0.0),
            wy=ang.get('y', 0.0),
            wz=ang.get('z', 0.0),
            ax=acc.get('x', 0.0),
            ay=acc.get('y', 0.0),
            az=acc.get('z', 0.0),
        )

    def _to_ros(self) -> dict:
        """
        Convert this IMU into a ROS-style dictionary.

        Returns
        -------
        dict
            Dictionary with ``orientation``, ``angular_velocity``,
            and ``linear_acceleration`` fields.
        """
        return {
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


class Bool:
    """
    Simple wrapper for the ROS ``std_msgs/Bool`` message type.

    Represents a boolean payload and provides helpers for converting
    to and from the ROS-style dictionary representation.

    Attributes
    ----------
    data : bool
        The boolean value contained in the message.
    """

    _ros_type = 'std_msgs/Bool'

    def __init__(self, data=False) -> None:
        self.data = data

    @classmethod
    def _from_ros(cls, msg: dict) -> 'Bool':
        """
        Create a ``Bool`` instance from a ROS-style dictionary.

        Parameters
        ----------
        msg : dict
            Dictionary containing a ``data`` key.

        Returns
        -------
        Bool
            Parsed Bool message.
        """
        return cls(data=msg.get('data', False))

    def _to_ros(self) -> dict:
        """
        Convert this message to a ROS-style dictionary.

        Returns
        -------
        dict
            ``{'data': bool}`` representation.
        """
        return {'data': self.data}


class String:
    """
    Simple wrapper for the ROS ``std_msgs/String`` message type.

    Represents a single string payload and provides helpers for converting
    to and from ROS-style dictionary representations.

    Attributes
    ----------
    data : str
        The string payload contained in the message.
    """

    _ros_type = 'std_msgs/String'

    def __init__(self, data: str = '') -> None:
        self.data = data

    @classmethod
    def _from_ros(cls, msg: dict) -> 'String':
        """
        Create a ``String`` instance from a ROS-style dictionary.

        Parameters
        ----------
        msg : dict
            Dictionary containing a ``data`` key.

        Returns
        -------
        String
            Parsed string message.
        """
        return cls(data=msg.get('data', ''))

    def _to_ros(self) -> dict:
        """
        Convert this message to a ROS-style dictionary.

        Returns
        -------
        dict
            ``{'data': str}`` representation.
        """
        return {'data': self.data}
