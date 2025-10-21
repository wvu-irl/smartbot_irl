# converters.py
"""
Convert from roslibpys dict-ified ros2 messages into our data classes. When adding messages that use new types make a new `from_<type>` here.
"""

from scipy.spatial.transform import Rotation as R
import numpy as np
from .type_maps import Pose, PoseArray, LaserScan, JointState, IMU, Bool, String


def from_pose(msg: dict) -> Pose:
    pose = msg["pose"]["pose"]
    pos = pose["position"]
    ori = pose["orientation"]

    qx = ori.get("x", 0.0)
    qy = ori.get("y", 0.0)
    qz = ori.get("z", 0.0)
    qw = ori.get("w", 1.0)
    quat = np.array([qx, qy, qz, qw])

    euler = R.from_quat(quat).as_euler("xyz", degrees=False)
    roll, pitch, yaw = euler

    # Quat -> euler.
    euler = R.from_quat(quat).as_euler("xyz", degrees=False)
    roll, pitch, yaw = euler
    return Pose(
        x=pos.get("x", 0.0),
        y=pos.get("y", 0.0),
        z=pos.get("z", 0.0),
        qx=qx,
        qy=qy,
        qz=qz,
        qw=qw,
        roll=roll,
        pitch=pitch,
        yaw=yaw,
    )


def from_laserscan(msg: dict) -> LaserScan:
    return LaserScan(
        ranges=msg.get("ranges", []),
        angle_min=msg.get("angle_min", 0.0),
        angle_max=msg.get("angle_max", 0.0),
        angle_increment=msg.get("angle_increment", 0.0),
    )


def from_jointstate(msg: dict) -> JointState:
    return JointState(
        names=msg.get("name", []),
        positions=msg.get("position", []),
        velocities=msg.get("velocity", []),
    )


def from_posearray(msg: dict) -> PoseArray:
    poses = []
    for p in msg.get("poses", []):
        pos = p["position"]
        ori = p["orientation"]

        qx = ori.get("x", 0.0)
        qy = ori.get("y", 0.0)
        qz = ori.get("z", 0.0)
        qw = ori.get("w", 1.0)
        quat = np.array([qx, qy, qz, qw])

        roll, pitch, yaw = R.from_quat(quat).as_euler("xyz", degrees=False)

        poses.append(
            Pose(
                x=pos.get("x", 0.0),
                y=pos.get("y", 0.0),
                z=pos.get("z", 0.0),
                qx=qx,
                qy=qy,
                qz=qz,
                qw=qw,
                roll=roll,
                pitch=pitch,
                yaw=yaw,
            )
        )

    return PoseArray(poses=poses)


def from_imu(msg: dict) -> IMU:
    return IMU(
        orientation=msg.get("orientation", {}),
        angular_velocity=msg.get("angular_velocity", {}),
        linear_acceleration=msg.get("linear_acceleration", {}),
    )


def from_bool(msg: dict) -> Bool:
    return Bool(
        data=msg.get("data", False),
    )


def from_string(msg: dict) -> String:
    return String(
        data=msg.get("data", ""),
    )

def from_odometry(msg: dict) -> Pose:
    pose = msg["pose"]["pose"]
    pos = pose["position"]
    ori = pose["orientation"]

    qx = ori.get("x", 0.0)
    qy = ori.get("y", 0.0)
    qz = ori.get("z", 0.0)
    qw = ori.get("w", 1.0)
    quat = np.array([qx, qy, qz, qw])

    roll, pitch, yaw = R.from_quat(quat).as_euler("xyz", degrees=False)

    return Pose(
        x=pos.get("x", 0.0),
        y=pos.get("y", 0.0),
        z=pos.get("z", 0.0),
        qx=qx,
        qy=qy,
        qz=qz,
        qw=qw,
        roll=roll,
        pitch=pitch,
        yaw=yaw,
    )


# Map from ros2 message type to converter func handle.
# Don't forget to add register message maps here!
ROS_TYPE_MAP = {
    "nav_msgs/Odometry": from_odometry,
    "geometry_msgs/Pose": from_pose,
    "sensor_msgs/LaserScan": from_laserscan,
    "sensor_msgs/JointState": from_jointstate,
    "geometry_msgs/PoseArray": from_posearray,
    "sensor_msgs/Imu": from_imu,
    "std_msgs/Bool": from_bool,
    "std_msgs/String": from_string,
}
