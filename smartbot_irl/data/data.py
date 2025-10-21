# data.py
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .type_maps import IMU, JointState, LaserScan, Pose, PoseArray, Bool, String, Odometry


class SensorData:
    """
    Container for all SmartBot sensor topics.
    Each field starts as ``None`` and becomes a populated message
    object (LaserScan, Odometry, etc.) once that topic is received.
    """

    def __init__(self) -> None:
        self.odom: Optional[Odometry] = None
        self.scan: Optional[LaserScan] = None
        self.joints: Optional[JointState] = None
        self.aruco_poses:PoseArray = None
        self.imu: Optional[IMU] = None
        self.gripper_curr_state: Optional[String] = None
        self.manipulator_curr_preset: Optional[String] = None
        self.seen_hexes: Optional[PoseArray] = None
        self.seen_robots: Optional[PoseArray] = None

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
