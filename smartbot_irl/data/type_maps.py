# smartbot_irl/data/type_maps.py
from dataclasses import dataclass, field
from typing import List, Dict
from scipy.spatial.transform import Rotation as R
import numpy as np


# ------------------------------------------------------------
# Geometry and Basic Pose Types
# ------------------------------------------------------------
@dataclass
class Pose:
    ros_type = "geometry_msgs/Pose"

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

    @classmethod
    def from_ros(cls, msg: dict):
        pos = msg.get("position", {})
        ori = msg.get("orientation", {})
        q = np.array(
            [
                ori.get("x", 0.0),
                ori.get("y", 0.0),
                ori.get("z", 0.0),
                ori.get("w", 1.0),
            ]
        )
        roll, pitch, yaw = R.from_quat(q).as_euler("xyz", degrees=False)
        return cls(
            x=pos.get("x", 0.0),
            y=pos.get("y", 0.0),
            z=pos.get("z", 0.0),
            qx=q[0],
            qy=q[1],
            qz=q[2],
            qw=q[3],
            roll=roll,
            pitch=pitch,
            yaw=yaw,
        )

    def to_ros(self):
        return {
            "position": {"x": self.x, "y": self.y, "z": self.z},
            "orientation": {"x": self.qx, "y": self.qy, "z": self.qz, "w": self.qw},
        }


# ------------------------------------------------------------
@dataclass
class Odometry:
    ros_type = "nav_msgs/Odometry"

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

    @classmethod
    def from_ros(cls, msg: dict):
        pose = msg.get("pose", {}).get("pose", {})
        pos = pose.get("position", {})
        ori = pose.get("orientation", {})
        q = np.array(
            [
                ori.get("x", 0.0),
                ori.get("y", 0.0),
                ori.get("z", 0.0),
                ori.get("w", 1.0),
            ]
        )
        roll, pitch, yaw = R.from_quat(q).as_euler("xyz", degrees=False)

        twist = msg.get("twist", {}).get("twist", {})
        lin = twist.get("linear", {})
        ang = twist.get("angular", {})

        return cls(
            x=pos.get("x", 0.0),
            y=pos.get("y", 0.0),
            z=pos.get("z", 0.0),
            qx=q[0],
            qy=q[1],
            qz=q[2],
            qw=q[3],
            roll=roll,
            pitch=pitch,
            yaw=yaw,
            vx=lin.get("x", 0.0),
            vy=lin.get("y", 0.0),
            vz=lin.get("z", 0.0),
            wx=ang.get("x", 0.0),
            wy=ang.get("y", 0.0),
            wz=ang.get("z", 0.0),
        )

    def to_ros(self):
        return {
            "pose": {
                "pose": {
                    "position": {"x": self.x, "y": self.y, "z": self.z},
                    "orientation": {"x": self.qx, "y": self.qy, "z": self.qz, "w": self.qw},
                }
            },
            "twist": {
                "twist": {
                    "linear": {"x": self.vx, "y": self.vy, "z": self.vz},
                    "angular": {"x": self.wx, "y": self.wy, "z": self.wz},
                }
            },
        }


# ------------------------------------------------------------
@dataclass
class PoseArray:
    ros_type = "geometry_msgs/PoseArray"
    poses: List[Pose] = field(default_factory=list)

    @classmethod
    def from_ros(cls, msg: dict):
        poses = [Pose.from_ros(p) for p in msg.get("poses", [])]
        return cls(poses=poses)

    def to_ros(self):
        return {"poses": [p.to_ros() for p in self.poses]}


# ------------------------------------------------------------
@dataclass
class LaserScan:
    """
    Represents a 2D planar laser scan message.

    This class mirrors the fields of :msg:`sensor_msgs/LaserScan` and provides
    conversion helpers to and from ROS dictionary form.

    Attributes
    ----------
    ros_type : str
        The ROS message type string (`"sensor_msgs/LaserScan"`).

    ranges : list of float
        Range readings from the laser in meters. Each value corresponds to a
        beam.

    angle_min : float
        Start angle of the scan, in radians (usually negative).

    angle_max : float
        End angle of the scan, in radians.

    angle_increment : float
        Angular distance between successive measurements, in radians.
    """

    ros_type = "sensor_msgs/LaserScan"

    ranges: List[float] = field(default_factory=list)
    angle_min: float = 0.0
    angle_max: float = 0.0
    angle_increment: float = 0.0

    @classmethod
    def from_ros(cls, msg: dict):
        return cls(
            ranges=msg.get("ranges", []),
            angle_min=msg.get("angle_min", 0.0),
            angle_max=msg.get("angle_max", 0.0),
            angle_increment=msg.get("angle_increment", 0.0),
        )

    def to_ros(self):
        return {
            "ranges": self.ranges,
            "angle_min": self.angle_min,
            "angle_max": self.angle_max,
            "angle_increment": self.angle_increment,
        }


# ------------------------------------------------------------
@dataclass
class JointState:
    ros_type = "sensor_msgs/JointState"
    names: List[str] = field(default_factory=list)
    positions: List[float] = field(default_factory=list)
    velocities: List[float] = field(default_factory=list)

    @classmethod
    def from_ros(cls, msg: dict):
        return cls(
            names=msg.get("name", []),
            positions=msg.get("position", []),
            velocities=msg.get("velocity", []),
        )

    def to_ros(self):
        return {
            "name": self.names,
            "position": self.positions,
            "velocity": self.velocities,
        }


# ------------------------------------------------------------
@dataclass
class IMU:
    ros_type = "sensor_msgs/Imu"
    orientation: Dict[str, float] = field(default_factory=dict)
    angular_velocity: Dict[str, float] = field(default_factory=dict)
    linear_acceleration: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_ros(cls, msg: dict):
        return cls(
            orientation=msg.get("orientation", {}),
            angular_velocity=msg.get("angular_velocity", {}),
            linear_acceleration=msg.get("linear_acceleration", {}),
        )


# ------------------------------------------------------------
@dataclass
class Bool:
    ros_type = "std_msgs/Bool"
    data: bool = False

    @classmethod
    def from_ros(cls, msg: dict):
        return cls(data=msg.get("data", False))

    def to_ros(self):
        return {"data": self.data}


# ------------------------------------------------------------
@dataclass
class String:
    ros_type = "std_msgs/String"
    data: str = ""

    @classmethod
    def from_ros(cls, msg: dict):
        return cls(data=msg.get("data", ""))

    def to_ros(self):
        return {"data": self.data}
