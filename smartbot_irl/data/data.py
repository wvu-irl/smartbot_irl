# data.py
import os
import time
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any, Dict, List, Optional

from .type_maps import IMU, JointState, LaserScan, Pose, PoseArray, Bool, String, Odometry

# def _flatten_value(prefix: str, obj: Any) -> Dict[str, Any]:
#     """
#     Recursively flatten a dataclass, dict, list, or primitive value.
#     Returns { "prefix_field_subfield": value, ... }
#     """
#     flat = {}

#     # Nothing here → skip
#     if obj is None:
#         return flat

#     # Dataclass → expand fields
#     if is_dataclass(obj):
#         for f in fields(obj):
#             sub = getattr(obj, f.name)
#             key = f"{prefix}_{f.name}"
#             flat.update(_flatten_value(key, sub))
#         return flat

#     # Dict → expand keys
#     if isinstance(obj, dict):
#         for k, v in obj.items():
#             key = f"{prefix}_{k}"
#             flat.update(_flatten_value(key, v))
#         return flat

#     # Lists / tuples
#     if isinstance(obj, (list, tuple)):
#         for i, v in enumerate(obj):
#             key = f"{prefix}_{i}"
#             flat.update(_flatten_value(key, v))
#         return flat

#     # Base case → primitive value
#     flat[prefix] = obj
#     return flat

def list_sensor_columns() -> list[str]:
    """Return top-level keys from flatten()."""
    s = SensorData.initialized()
    return list(s.flatten().keys())
    
def flatten_generic(prefix: str, obj: Any) -> Dict[str, Any]:
    """
    Flatten dataclasses and dicts.
    Leave lists/tuples intact as a single object.
    """
    flat = {}

    if obj is None:
        return flat

    # Dataclass → expand fields
    if is_dataclass(obj):
        for f in fields(obj):
            val = getattr(obj, f.name)
            key = f"{prefix}_{f.name}"
            flat.update(flatten_generic(key, val))
        return flat

    # Dict → expand key/value pairs
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}_{k}"
            flat.update(flatten_generic(key, v))
        return flat

    # Lists / tuples → DO NOT flatten, store as whole object
    if isinstance(obj, (list, tuple)):
        flat[prefix] = obj
        return flat

    # Primitive value
    flat[prefix] = obj
    return flat

class SensorData:
    """
    Container for all SmartBot sensor topics.
    Each field starts as ``None`` and becomes a populated message
    object (LaserScan, Odometry, etc.) once that topic is received.
    """

    def __init__(self) -> None:
        self.odom = Odometry()
        self.scan = LaserScan()
        self.joints = JointState()
        self.aruco_poses = PoseArray()
        self.imu = IMU()
        self.gripper_curr_state = String()
        self.manipulator_curr_preset = String()
        self.seen_hexes = PoseArray()
        self.seen_robots = PoseArray()

    @classmethod
    def initialized(cls) -> "SensorData":
        """
        Return a new SensorData with all message objects constructed using
        their default constructors. Useful for simulation environments
        where we don't wait for ROS topics to populate.
        """
        self = cls()
        self.odom = Odometry()
        self.scan = LaserScan()
        self.joints = JointState()
        self.aruco_poses = PoseArray()
        self.imu = IMU()
        self.gripper_curr_state = String()
        self.manipulator_curr_preset = String()
        self.seen_hexes = PoseArray()
        self.seen_robots = PoseArray()
        return self
    # ------------------------------------------------------------------
    def to_ros(self) -> dict:
        """Convert only populated fields to ROS-like dicts."""
        d = {}
        if self.odom:
            d["odom"] = self.odom.to_ros()
        if self.scan:
            d["scan"] = self.scan.to_ros()
        if self.joints:
            d["joints"] = self.joints.to_ros()
        if self.aruco_poses:
            d["aruco_poses"] = self.aruco_poses.to_ros()
        if self.imu:
            d["imu"] = self.imu.__dict__
        if self.gripper_curr_state:
            d["gripper_curr_state"] = self.gripper_curr_state.to_ros()
        if self.manipulator_curr_preset:
            d["manipulator_curr_preset"] = self.manipulator_curr_preset.to_ros()
        if self.seen_hexes:
            d["seen_hexes"] = self.seen_hexes.to_ros()
        if self.seen_robots:
            d["seen_robots"] = self.seen_robots.to_ros()
        return d

    def __repr__(self):
        keys = [k for k, v in vars(self).items() if v is not None]
        missing = [k for k, v in vars(self).items() if v is None]
        return f"SensorData(populated={keys}, missing={missing})"
    def flatten(self) -> dict:
        """Return a fully flattened dict of all sensor fields."""
        out = {}
        for name, value in vars(self).items():
            out.update(flatten_generic(name, value))
        return out



@dataclass
class Command:
    """
    High-level command for SmartBot.

    Supports both:
      - Differential drive control (linear + angular velocity)
      - Direct wheel velocity control (left/right)
      - Manipulator preset and gripper control
    """

    wheel_vel_left: Optional[float] = None
    wheel_vel_right: Optional[float] = None
    linear_vel: Optional[float] = None
    angular_vel: Optional[float] = None
    gripper_closed: Optional[bool] = None
    manipulator_presets: Optional[str] = None

    # -------------------------------------------------------------
    def to_ros(self) -> dict:
        """
        Convert this Command into a dictionary that rosliby can publish.
        """
        msgs = {}

        # velocity command (Twist)
        if self.linear_vel is not None or self.angular_vel is not None:
            msgs["geometry_msgs/Twist"] = {
                "linear": {"x": self.linear_vel or 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": self.angular_vel or 0.0},
            }

        # manipulator preset (String)
        if self.manipulator_presets is not None:
            msgs["std_msgs/String"] = {"data": str(self.manipulator_presets)}

        # gripper state (Bool)
        if self.gripper_closed is not None:
            msgs["std_msgs/Bool"] = {"data": bool(self.gripper_closed)}

        return msgs
