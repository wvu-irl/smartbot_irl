# smartbot_real.py
import os
import time
from pathlib import Path
from typing import Optional

import yaml

from .smartbot_base import SmartBotBase
from ..data._converters import ROS_TYPE_MAP
from ..data._type_maps import (
    ArucoMarkers,
    Odometry,
    LaserScan,
    JointState,
    PoseArray,
    IMU,
    Bool,
    String,
)

os.environ['AUTOBAHN_USE_NVX'] = '0'
import threading
from dataclasses import dataclass, field

import roslibpy

from ..data import Command, Pose, SensorData
from ..drawing import Drawer
from smartbot_irl.utils import SmartLogger
import logging

logger = SmartLogger(level=logging.INFO)  # Print statements, but better!


class SmartBotReal(SmartBotBase):
    """
    Wrapper for the real robot's ros2 system.
    """

    # def __init__(self, drawing=(), smartbot_num=0,) -> None:
    def __init__(self, drawing=False, smartbot_num=0, draw_region=((-5, 5), (-5, 5))):
        super().__init__(drawing=drawing, draw_region=draw_region)

        self.drawer = Drawer(lambda: self.sensor_data, region=draw_region) if drawing else None
        self._running = False
        self.smartbot_num = smartbot_num
        print(f'my num is {self.smartbot_num}')
        self.client: roslibpy.Ros | None = None
        self._connected = threading.Event()

        # Specify which topics and their types we will subscribe to.
        self.sensor_data = SensorData()
        self._topic_map = {  # "<ros2_topic_name>": (<type_maps.Pose>, "<SensorData.field>")
            'odom': (Odometry, 'odom'),
            'scan': (LaserScan, 'scan'),
            'joint_states': (JointState, 'joints'),
            'aruco_poses': (PoseArray, 'aruco_poses'),
            'livox/imu': (IMU, 'imu'),
            'gripper_curr_state': (String, 'gripper_curr_state'),
            'manipulator_curr_preset': (String, 'manipulator_curr_preset'),
            'seen_robots': (PoseArray, 'seen_robots'),
            'seen_hexes': (ArucoMarkers, 'seen_hexes'),
        }

        # Keep a list of our connected topics.
        self._subscriptions: list[roslibpy.Topic] = []

        # Publishers.
        self.cmd_vel_pub: Optional[roslibpy.Topic] = None
        self.manipulator_presets_pub: Optional[roslibpy.Topic] = None
        self.gripper_closed_pub: Optional[roslibpy.Topic] = None
        self.place_hex_pub: Optional[roslibpy.Topic] = None

    def init(self, host: str = 'localhost', port: int = 9090, yaml_path=None) -> None:
        """Connect the smartbot wrapper to a real smartbot.

        Args:
            host (str, optional):
                IP address/hostname of a smartbot running rosbridge_server to
                connect to. Default is to try and connect to a rosbridge running
                on the localhost. Usually this is replaced by the IP address of
                the smartbot on your local network (e.g. `192.168.33.2`).

            port (int, optional):
                What port to try and connect to the rosbridge on. The
                rosbridge_server node defaults to 9090.
        """
        prefix = f'/smartbot{self.smartbot_num}'
        self._running = True

        # Connect to ros bridge server. Give up after 5s.
        logger.info(msg='Connecting to smartbot...')
        self.client = roslibpy.Ros(host=host, port=port, is_secure=False)
        self.client.on_ready(self._connected.set)
        self.client.run()
        logger.info(f'Connecting to rosbridge at ws://{host}:{port} ...')
        self._connected.wait(timeout=5.0)

        if not self.client.is_connected:
            logger.error(msg='Could not connect to smartbot!')
            raise RuntimeError('Failed to connect to rosbridge_server.')

        # Set up publishers.
        self.cmd_vel_pub = roslibpy.Topic(
            self.client,
            prefix + '/cmd_vel',
            'geometry_msgs/Twist',
        )
        self.manipulator_presets_pub = roslibpy.Topic(
            self.client,
            prefix + '/manipulator_presets',
            'std_msgs/String',
        )
        self.gripper_closed_pub = roslibpy.Topic(
            self.client,
            prefix + '/gripper_closed',
            'std_msgs/Bool',
        )
        self.place_hex_pub = roslibpy.Topic(
            self.client,
            prefix + '/place_hex',
            'geometry_msgs/Pose',
        )

        # Set up subscribers.
        for name, (cls, field_name) in self._topic_map.items():
            topic = roslibpy.Topic(self.client, f'{prefix}/{name}', cls.ros_type)
            topic.subscribe(
                lambda msg, f=field_name, c=cls: setattr(self.sensor_data, f, c.from_ros(msg))
            )
        print(f'Subscribers and publishers found for {prefix}/* topics')

    def place_hex(self, x=None, y=None):
        """Place a new hex marker at a random or specified world position."""
        if not self.client or not self.client.is_connected:
            print('Cannot place hex: ROSBridge not connected.')
            return

        if x is None or y is None:
            # randomize within a 3x3 meter box centered at origin
            import random

            x = random.uniform(-3.0, 3.0)
            y = random.uniform(-3.0, 3.0)

        msg = {
            'position': {'x': float(x), 'y': float(y), 'z': 0.0},
            'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 1.0},
        }
        self.place_hex_pub.publish(roslibpy.Message(msg))
        print(f'Placed hex at ({x:.2f}, {y:.2f})')

    # Publish messages.
    def write(self, cmd: Command):
        """Publish the contents of :param:`cmd` to Ros2.

        Args:
            cmd (:class:`smartbot_irl.Command`):
                An instance of :class:`smartbot_irl.Command` which should
                be populated with values to be published.
        """
        if not self.client or not self.client.is_connected:
            print('Not connected to ROSBridge; cannot publish command.')
            return

        assert self.cmd_vel_pub is not None  # TODO make a mapping for this and loop for asserts.
        assert self.manipulator_presets_pub is not None
        assert self.gripper_closed_pub is not None

        msgs = cmd.to_ros()

        if 'geometry_msgs/Twist' in msgs:
            self.cmd_vel_pub.publish(roslibpy.Message(msgs['geometry_msgs/Twist']))

        if 'std_msgs/String' in msgs:
            self.manipulator_presets_pub.publish(roslibpy.Message(msgs['std_msgs/String']))

        if 'std_msgs/Bool' in msgs:
            self.gripper_closed_pub.publish(roslibpy.Message(msgs['std_msgs/Bool']))

    # -----------------------------------------------------------------
    def read(self) -> SensorData:
        """Return the most recently received sensor data."""
        return self.sensor_data

    # -----------------------------------------------------------------
    def spin(self, dt: float = 0.01) -> None:
        """"""
        if not self.client or not self.client.is_connected:
            raise RuntimeError('ROSBridge client not connected.')
        if self.drawer and self.drawer._running:
            self.drawer.draw_once(dt)
        # time.sleep(dt)

    # -----------------------------------------------------------------
    def shutdown(self) -> None:
        """Cleanly disconnect all topics, publishers, and client."""
        print('Shutting down SmartBotReal...')

        # Unsubscribe all topics.
        for topic in self._subscriptions:
            try:
                topic.unsubscribe()
            except Exception as e:
                print(f'Warning: failed to unsubscribe {topic.name}: {e}')
        self._subscriptions.clear()

        # Stop publishers.
        for pub in [self.cmd_vel_pub, self.gripper_closed_pub]:
            if pub:
                try:
                    pub.unadvertise()
                except Exception:
                    pass

        # Close client connection.
        if self.client:
            try:
                if self.client.is_connected:
                    self.client.terminate()
                self.client.close()
            except Exception as e:
                print(f'Error closing client: {e}')
            finally:
                self.client = None

        # Shut down drawer if any.
        if self.drawer:
            try:
                self.drawer.quit()
            except Exception:
                pass

        self._running = False
        print('SmartBotReal shutdown complete.')


if __name__ == '__main__':
    bot = SmartBotReal(drawing=False)
    bot.init(host='localhost', port=9090)

    cmd = Command(
        wheel_vel_left=0.3,
        wheel_vel_right=0.3,
        gripper_closed=True,
        linear_vel=1,
        manipulator_presets='DOWN',
    )

    try:
        while True:
            bot.write(cmd)
            data = bot.read()
            print(data.__dict__.keys)
            # print(f"Odom: x={data.pose_x:.2f}, y={data.pose_y:.2f}, θ={data.pose_theta:.2f}")
            bot.spin(0.5)
    except KeyboardInterrupt:
        bot.shutdown()
