# smartbot_irl.data._data.py

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any, Dict, List

from smartbot_irl.ros_types.geometry_msgs.msg import PoseArray as RosPoseArray
from smartbot_irl.ros_types.nav_msgs.msg import Odometry as RosOdometry
from smartbot_irl.ros_types.sensor_msgs.msg import CompressedImage as RosCompressedImage
from smartbot_irl.ros_types.sensor_msgs.msg import Image as RosImage

# from smartbot_irl.ros_types.sensor_msgs.msg import Image as RosImage
from smartbot_irl.ros_types.sensor_msgs.msg import Imu as RosImu
from smartbot_irl.ros_types.sensor_msgs.msg import JointState as RosJointState
from smartbot_irl.ros_types.sensor_msgs.msg import LaserScan as RosLaserScan
from smartbot_irl.ros_types.std_msgs.msg import String as RosString
from smartbot_irl.types import (
    ArucoMarkers,
    BaseType,
    Imu,
    Joints,
    LaserScan,
    Odometry,
    PoseArray,
    String,
)

from ..types._base_type import BaseType


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


@dataclass
class RawSensorData:
    odom: RosOdometry | None = None
    scan: RosLaserScan | None = None
    joints: RosJointState | None = None
    aruco_poses: RosPoseArray | None = None
    imu: RosImu | None = None
    gripper_curr_state: RosString | None = None
    manipulator_curr_preset: RosString | None = None
    seen_robots: RosPoseArray | None = None


@dataclass
class SensorData:
    raw: RawSensorData = field(default_factory=RawSensorData)
    odom: Odometry = field(default_factory=Odometry)
    scan: LaserScan = field(default_factory=LaserScan)
    joints: Joints = field(default_factory=Joints)
    seen_hexes: PoseArray = field(default_factory=PoseArray)
    imu: Imu = field(default_factory=Imu)
    gripper_curr_state: String = field(default_factory=String)
    manipulator_curr_preset: String = field(default_factory=String)
    seen_robots: PoseArray = field(default_factory=PoseArray)

    @classmethod
    def initialized(cls) -> 'SensorData':
        return cls()

    def to_ros(self) -> dict:
        result = {}

        # Iterate through all the attr of the object.
        # This is maybe a bad idea since it means we can't add any attributes that aren't ros2type mappable...
        # Could check if each attr has .to_ros, but that is also silly...
        for f in fields(self):
            if f.name == 'raw':
                continue

            value = getattr(self, f.name)

            if value is not None:
                result[f.name] = value.to_ros()

        return result

    def __repr__(self) -> str:
        populated = []
        missing = []

        for f in fields(self):
            if f.name == 'raw':
                continue

            value = getattr(self, f.name)

            if value is None:
                missing.append(f.name)
            else:
                populated.append(f.name)

        return f'SensorData(populated={populated}, missing={missing})'

    def flatten(self) -> dict[str, Any]:
        out = {}

        for f in fields(self):
            if f.name == 'raw':
                continue

            value = getattr(self, f.name)

            out.update(
                flatten_generic(
                    f.name,
                    value,
                )
            )

        return out


@dataclass(frozen=True)
class SensorSpec:
    type: type[BaseType]
    ros_type: type[Any]
    ros_topic: str
    timeout: float


SENSORS = {
    'odom': SensorSpec(
        type=Odometry,
        ros_type=RosOdometry,
        ros_topic='odom',
        timeout=5.0,
    ),
    'aruco_poses': SensorSpec(
        type=PoseArray,
        ros_type=RosPoseArray,
        ros_topic='aruco_poses',
        timeout=0.25,
    ),
    'seen_robots': SensorSpec(
        type=PoseArray,
        ros_type=RosPoseArray,
        ros_topic='seen_robots',
        timeout=0.5,
    ),
    'joints': SensorSpec(
        type=Joints,
        ros_type=RosJointState,
        ros_topic='joint_states',
        timeout=0.1,
    ),
    'seen_hexes': SensorSpec(
        type=PoseArray,
        ros_type=RosPoseArray,
        ros_topic='seen_hexes',
        timeout=0.2,
    ),
    'imu': SensorSpec(
        type=Imu,
        ros_type=RosImu,
        ros_topic='livox/imu',
        timeout=0.2,
    ),
    'scan': SensorSpec(
        type=LaserScan,
        ros_type=RosLaserScan,
        ros_topic='scan',
        timeout=0.2,
    ),
}


@dataclass
class Command:
    """
    High-level command for SmartBot.
    Twist and indiv whele control.
    """

    wheel_vel_left: float | None = 0.0
    wheel_vel_right: float | None = 0.0
    linear_vel: float | None = 0.0
    angular_vel: float | None = 0.0
    gripper_closed: bool | None = None
    manipulator_presets: str | None = None
    reset_position: bool = False
    remove_bias: bool = False

    def to_ros(self) -> dict[str, dict[str, Any]]:
        msgs = {}

        if self.linear_vel is not None or self.angular_vel is not None:
            msgs['cmd_vel'] = {
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

        if self.manipulator_presets is not None:
            msgs['manipulator_presets'] = {'data': self.manipulator_presets}

        if self.gripper_closed is not None:
            msgs['gripper_closed'] = {'data': self.gripper_closed}

        if self.reset_position and self.remove_bias:
            raise ValueError('Conflicting position reset commands')

        if self.reset_position or self.remove_bias:
            msgs['pos_reset'] = {'data': self.remove_bias}

        return msgs


@dataclass(frozen=True)
class CommandSpec:
    topic: str
    ros_type: str


COMMANDS = {
    'cmd_vel': CommandSpec(
        topic='cmd_vel',
        ros_type='geometry_msgs/Twist',
    ),
    'manipulator_presets': CommandSpec(
        topic='manipulator_presets',
        ros_type='std_msgs/String',
    ),
    'gripper_closed': CommandSpec(
        topic='gripper_closed',
        ros_type='std_msgs/Bool',
    ),
    'pos_reset': CommandSpec(
        topic='pos_reset',
        ros_type='example_interfaces/Bool',
    ),
}
