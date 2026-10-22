# from __future__ import annotations

# from dataclasses import dataclass
# from typing import Any

# from smartbot_irl.data._data import RosImage
# from smartbot_irl.ros_types.geometry_msgs.msg import PoseArray as RosPoseArray
# from smartbot_irl.ros_types.nav_msgs.msg import Odometry as RosOdometry
# from smartbot_irl.ros_types.sensor_msgs.msg import CompressedImage as RosCompressedImage
# from smartbot_irl.ros_types.sensor_msgs.msg import (
#     Imu as RosImu,
# )
# from smartbot_irl.ros_types.sensor_msgs.msg import (
#     JointState as RosJointState,
# )
# from smartbot_irl.ros_types.sensor_msgs.msg import (
#     LaserScan as RosLaserScan,
# )
# from smartbot_irl.ros_types.std_msgs.msg import String as RosString
# from smartbot_irl.types import (
#     Imu,
#     Joints,
#     LaserScan,
#     Odometry,
#     PoseArray,
#     String,
# )
# from smartbot_irl.data import SensorData

# """
# root@smartbot4:/hardware_software# ros2 topic list
# /parameter_events
# /robot_state
# /rosout
# /smartbot4/arm_position_control
# /smartbot4/aruco_markers
# /smartbot4/aruco_poses
# /smartbot4/back_camera/compressed
# /smartbot4/back_camera/compressedDepth
# /smartbot4/back_camera/image_raw
# /smartbot4/back_camera/theora
# /smartbot4/back_camera/zstd
# /smartbot4/camera_info
# /smartbot4/client_count
# /smartbot4/cmd_vel
# /smartbot4/connected_clients
# /smartbot4/drive_goal_joints
# /smartbot4/front_camera/compressed
# /smartbot4/front_camera/compressedDepth
# /smartbot4/front_camera/image_raw
# /smartbot4/front_camera/theora
# /smartbot4/front_camera/zstd
# /smartbot4/gripper_closed
# /smartbot4/gripper_curr_state
# /smartbot4/heart_beat
# /smartbot4/internal_state
# /smartbot4/joint_states
# /smartbot4/joy
# /smartbot4/joy/set_feedback
# /smartbot4/livox/imu
# /smartbot4/livox/lidar
# /smartbot4/manipulator_curr_preset
# /smartbot4/manipulator_goal_joints
# /smartbot4/manipulator_presets
# /smartbot4/odom
# /smartbot4/pos_reset
# /smartbot4/reboot_motors
# /smartbot4/scan
# /smartbot4/seen_hexes
# /smartbot4/seen_robots
# /smartbot4/torque_on
# /tf
# /tf_static
# """


# @dataclass(frozen=True)
# class SensorSpec:
#     type: type[Any]
#     ros_type: type[Any]
#     topic: str
#     timeout: float
#     smart_name: type[Any]


# SENSORS = {
#     'odom': SensorSpec(
#         type=Odometry,
#         ros_type=RosOdometry,
#         topic='odom',
#         timeout=5.0,
#         smart_name=SensorData.odom
#     ),
#     'scan': SensorSpec(
#         type=LaserScan,
#         ros_type=RosLaserScan,
#         topic='scan',
#         timeout=5.0,
#     ),
#     'joints': SensorSpec(
#         type=Joints,
#         ros_type=RosJointState,
#         topic='joint_states',
#         timeout=1.0,
#     ),
#     'aruco_poses': SensorSpec(
#         type=PoseArray,
#         ros_type=RosPoseArray,
#         topic='aruco_poses',
#         timeout=0.25,
#     ),
#     'imu': SensorSpec(
#         type=Imu,
#         ros_type=RosImu,
#         topic='livox/imu',
#         timeout=0.25,
#     ),
#     'gripper_curr_state': SensorSpec(
#         type=String,
#         ros_type=RosString,
#         topic='gripper_curr_state',
#         timeout=3.0,
#     ),
#     'manipulator_curr_preset': SensorSpec(
#         type=String,
#         ros_type=RosString,
#         topic='manipulator_curr_preset',
#         timeout=3.0,
#     ),
#     'seen_robots': SensorSpec(
#         type=PoseArray,
#         ros_type=RosPoseArray,
#         topic='seen_robots',
#         timeout=0.5,
#     ),
#     # 'camera': SensorSpec(
#     #     type=RosCompressedImage,
#     #     ros_type=RosCompressedImage,
#     #     topic='front_camera/compressed',
#     #     timeout=0.5,
#     # ),
# }
