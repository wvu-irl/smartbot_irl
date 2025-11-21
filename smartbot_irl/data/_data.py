from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict, Optional

from .type_maps import (
    IMU,
    ArucoMarkers,
    Bool,
    JointState,
    LaserScan,
    Odometry,
    Pose,
    PoseArray,
    String,
)


def list_sensor_columns() -> list[str]:
    """Return top-level keys from flatten()."""
    s = SensorData()
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
            key = f'{prefix}_{f.name}'
            flat.update(flatten_generic(key, val))
        return flat

    # Dict → expand key/value pairs
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f'{prefix}_{k}'
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

    Each attribute stores one sensor message object. Instances start
    pre-initialized with empty message types; each message becomes
    populated as new data arrives.

    Attributes
    ----------
    odom : Odometry
        Robot odometry message.
    scan : LaserScan
        Planar LiDAR scan message.
    joints : JointState
        Joint states for the robot's manipulator or mechanisms.
    aruco_poses : PoseArray
        Detected ArUco marker poses.
    imu : IMU
        Inertial measurement message.
    gripper_curr_state : String
        Current gripper state.
    manipulator_curr_preset : String
        Name of the current manipulator preset.
    seen_hexes : ArucoMarkers
        Set of detected hexagonal field markers.
    seen_robots : PoseArray
        Poses of detected nearby robots.

    """

    def __init__(self) -> None:
        self.odom: Odometry = Odometry()
        self.scan: LaserScan = LaserScan()
        self.joints: JointState = JointState()
        self.aruco_poses: PoseArray = PoseArray()
        self.imu: IMU = IMU()
        self.gripper_curr_state: String = String()
        self.manipulator_curr_preset: String = String()
        self.seen_hexes: ArucoMarkers = ArucoMarkers()
        self.seen_robots: PoseArray = PoseArray()

    # ------------------------------------------------------------------
    def _to_ros(self) -> dict:
        """Convert only populated fields to ROS-like dicts."""
        d = {}
        if self.odom:
            d['odom'] = self.odom._to_ros()
        if self.scan:
            d['scan'] = self.scan._to_ros()
        if self.joints:
            d['joints'] = self.joints._to_ros()
        if self.aruco_poses:
            d['aruco_poses'] = self.aruco_poses._to_ros()
        if self.imu:
            d['imu'] = self.imu.__dict__
        if self.gripper_curr_state:
            d['gripper_curr_state'] = self.gripper_curr_state._to_ros()
        if self.manipulator_curr_preset:
            d['manipulator_curr_preset'] = self.manipulator_curr_preset._to_ros()
        if self.seen_hexes:
            d['seen_hexes'] = self.seen_hexes._to_ros()
        if self.seen_robots:
            d['seen_robots'] = self.seen_robots._to_ros()
        return d

    def __repr__(self):
        keys = [k for k, v in vars(self).items() if v is not None]
        missing = [k for k, v in vars(self).items() if v is None]
        return f'SensorData(populated={keys}, missing={missing})'

    def flatten(self) -> dict:
        """
        Return a flattened dictionary containing all sensor data fields.

        This method walks every attribute in the ``SensorData`` instance then
        applies ``flatten_generic`` to each, and merges the results into a
        single dictionary. Useful for saving/printing.

        Returns
        -------
        dict
            A dictionary where all sensor values are flattened into key–value
            pairs like:
             ``'odom_x'``, ``'scan_ranges'``, ``'imu_roll'``, etc.
        """
        out = {}
        for name, value in vars(self).items():
            out.update(flatten_generic(name, value))
        return out


class Command:
    """
    High-level command container for SmartBot control.

    Attributes
    ----------
    wheel_vel_left : float or None
        Left wheel velocity command.

    wheel_vel_right : float or None
        Right wheel velocity command.

    linear_vel : float or None
        Forward linear velocity in meters per second.

    angular_vel : float or None
        Angular velocity in radians per second (yaw rate).

    gripper_closed : bool or None
        ``True`` closes the gripper, ``False`` opens it.

    manipulator_presets : str or None
        Name of a manipulator preset to activate.

    Notes
    -----
    Only fields that are not ``None`` are sent to the ROS2 system.

    Examples
    --------
    Linear and angular velocity command:

    >>> cmd = Command(linear_vel=0.5, angular_vel=1.0)
    >>> bot.write(cmd)

    Change arm state:

    >>> cmd = Command(manipulator_presets='stow')
    """

    def __init__(
        self,
        wheel_vel_left: float = 0.0,
        wheel_vel_right: float = 0.0,
        linear_vel: float = 0.0,
        angular_vel: float = 0.0,
        gripper_closed: bool = False,
        manipulator_presets: str = 'STOW',
    ) -> None:
        # safe attribute initialization
        self.wheel_vel_left = wheel_vel_left
        self.wheel_vel_right = wheel_vel_right
        self.linear_vel = linear_vel
        self.angular_vel = angular_vel
        self.gripper_closed = gripper_closed
        self.manipulator_presets = manipulator_presets

    # -------------------------------------------------------------
    def _to_ros(self) -> dict:
        """
        Convert this ``Command`` instance into a ROS-style dictionary
        that ``roslibpy`` will take..

        Only fields with non-``None`` values are included.

        Returns
        -------
        dict
            A mapping of ROS message types to dictionaries.
        """
        msgs = {}

        # Differential drive (Twist)
        if self.linear_vel is not None or self.angular_vel is not None:
            msgs['geometry_msgs/Twist'] = {
                'linear': {
                    'x': self.linear_vel or 0.0,
                    'y': 0.0,
                    'z': 0.0,
                },
                'angular': {
                    'x': 0.0,
                    'y': 0.0,
                    'z': self.angular_vel or 0.0,
                },
            }

        # Manipulator preset (String)
        if self.manipulator_presets is not None:
            msgs['std_msgs/String'] = {'data': str(self.manipulator_presets)}

        # Gripper (Bool)
        if self.gripper_closed is not None:
            msgs['std_msgs/Bool'] = {'data': bool(self.gripper_closed)}

        return msgs
