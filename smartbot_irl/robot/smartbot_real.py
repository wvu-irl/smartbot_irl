# smartbot_real.py
import os

os.environ['AUTOBAHN_USE_NVX'] = '0'

import logging
import threading
import time
from typing import Optional

import roslibpy

from smartbot_irl.utils import SmartLogger

from ..data import Command, Pose, SensorData
from ..data._type_maps import (
    IMU,
    ArucoMarkers,
    Bool,
    JointState,
    LaserScan,
    Odometry,
    PoseArray,
    String,
)
from ..drawing import Drawer
from .smartbot_base import SmartBotBase

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

        # "<ros2_topic_name>": (<type_maps.Pose>, "<SensorData.field>")
        self._topic_map = {
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

        # Track last time we received a message for each SensorData field.
        self._last_msg_time: dict[str, float] = {
            field_name: 0.0 for (_, field_name) in self._topic_map.values()
        }

        # TODO make this adjustable. If timeout is faster than publish rate we get flickering data.
        self._timeout_sec = {
            'scan': 5.0,
            'odom': 5.0,
            'joints': 1.0,
            'aruco_poses': 0.25,
            'imu': 0.25,
            'gripper_curr_state': 3.0,
            'manipulator_curr_preset': 3.0,
            'seen_robots': 0.5,
            'seen_hexes': 0.5,
        }

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

        def make_callback(field_name, cls):
            """
            Make subscription callback and build dict of last reception time.
            Use this to wipe out messages that have gone stale.
            """

            def cb(msg):
                # Update sensor_data field.
                setattr(self.sensor_data, field_name, cls.from_ros(msg))
                # Update specific data's timestamp used to clear stale data.
                self._last_msg_time[field_name] = time.time()

            return cb

        # Now actually make the callbacks and store them.
        for name, (cls, field_name) in self._topic_map.items():
            topic = roslibpy.Topic(
                ros=self.client, name=f'{prefix}/{name}', message_type=cls.ros_type
            )
            topic.subscribe(callback=make_callback(field_name, cls))
            self._subscriptions.append(topic)

        print(f'Subscribers and publishers found for {prefix}/* topics')

    def write(self, cmd: Command):
        """Publish the contents of :param:`cmd` to Ros2.

        Parameters
        ----------
            cmd: :class:`smartbot_irl.Command`
                An instance of :class:`smartbot_irl.Command` which should be
                populated with values to be published.
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

    def read(self) -> SensorData:
        """Return current state of sensor data (after clearing stale fields).

        Uses the per-topic timeout limit specified in
        ``SmartBotReal._timeout_sec``and stored in
        ::dict::`SmartBotReal._last_msg_time` to replace any given sensor data
        attr with its initialized (empty) type. This is not the best way to
        solve this problem.

        Returns
        -------
        SensorData

        """
        now = time.time()

        # Check each topics time since last received and clear it if too long ago.
        for field_name, last_time in self._last_msg_time.items():
            timeout = self._timeout_sec.get(field_name, None)
            if timeout is None:
                continue

            if last_time != 0.0 and (now - last_time > timeout):
                data_type = type(getattr(self.sensor_data, field_name))
                setattr(self.sensor_data, field_name, data_type())
                self._last_msg_time[field_name] = 0.0  # Reset timer.

        return self.sensor_data

    # -----------------------------------------------------------------
    def spin(self, dt: float = 0.1) -> None:
        """
        Handle miscellanous tasks: Drawing, checking RosBridge health, ...

        Parameters
        ----------
        dt: float, default=0.1
            (seconds) How fast to flip the pygame display (Doesn't really work...)
        """
        if not self.client or not self.client.is_connected:
            raise RuntimeError('ROSBridge client not connected.')
        if self.drawer and self.drawer._running:
            self.drawer.draw_once(dt)

    # -----------------------------------------------------------------
    def shutdown(self) -> None:
        """Cleanly disconnect all topics, publishers, and rosbridge client."""
        print('Shutting down SmartBotReal...')
        cmd = Command(wheel_vel_left=0.0, wheel_vel_right=0.0, linear_vel=0.0, angular_vel=0.0)
        self.write(cmd)
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
