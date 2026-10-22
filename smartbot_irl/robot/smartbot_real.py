# smartbot_real.py
import os

from smartbot_irl.data._data import SensorSpec

os.environ['AUTOBAHN_USE_NVX'] = '0'

import logging
import threading
import time
from typing import List, Optional

import roslibpy

from smartbot_irl.conversion import from_dict

# from smartbot_irl.ros_py_mapping import SENSORS
from smartbot_irl.utils import SmartLogger

from ..data import COMMANDS, SENSORS, Command, SensorData
from ..drawing import Drawer
from .smartbot_base import SmartBotBase

logger = SmartLogger(level=logging.DEBUG)  # Print statements, but better!


class SmartBotReal(SmartBotBase):
    """
    Wrapper for the real robot's ros2 system.
    """

    # def __init__(self, drawing=(), smartbot_num=0,) -> None:
    def __init__(self, drawing=False, smartbot_num=0, draw_region=((-5, 5), (-5, 5))):
        super().__init__(drawing=drawing, draw_region=draw_region)

        # Create pygame drawer and give it reference to this robot's sensor data struct.
        self.drawer = Drawer(lambda: self.sensor_data, region=draw_region) if drawing else None
        self._running = False

        self.smartbot_num = smartbot_num
        print(f'my num is {self.smartbot_num}')

        self.client: roslibpy.Ros | None = None

        # Use this...
        self._connected = threading.Event()

        # Specify which topics and their types we will subscribe to.
        self.sensor_data = SensorData()

        # Keep a list of our connected topics.
        self._subscriptions: list[roslibpy.Topic] = []
        # self._publishers: list[roslibpy.Topic] = []
        self._publishers: dict[str, roslibpy.Topic] = {}

        # Keep track of last time we got a message on each sensor stream.
        self._last_msg_time = {field_name: 0.0 for field_name in SENSORS}

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
        prefix = f'smartbot{self.smartbot_num}'
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

        # set zero time
        self._last_msg_time = {field_name: 0.0 for field_name in SENSORS}

        for name, spec in COMMANDS.items():
            self._publishers[name] = roslibpy.Topic(
                ros=self.client,
                name=f'/{prefix}/{spec.topic}',
                message_type=spec.ros_type,
            )

        def make_callback(field_name: str, spec: SensorSpec):
            """func-factory. The field_name here needs match the SensorData attr. Param `spec` is used to setup the smart type conversion."""

            def cb(msg):
                raw = from_dict(spec.ros_type, msg)
                value = spec.type.from_ros(raw)

                setattr(self.sensor_data.raw, field_name, raw)
                setattr(self.sensor_data, field_name, value)

                self._last_msg_time[field_name] = time.monotonic()

            return cb

        # Make subscribers.
        # TODO: What do when SENSORS is malspecified?
        for field_name, spec in SENSORS.items():
            topic = roslibpy.Topic(
                ros=self.client,
                name=f'/{prefix}/{spec.ros_topic}',
                message_type=spec.ros_type.__msgtype__,
            )

            topic.subscribe(
                callback=make_callback(
                    field_name,
                    spec,
                )
            )

            self._subscriptions.append(topic)

    def place_hex(self):
        logger.error('Not implemented for real robots!')

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

        for name, msg in cmd.to_ros().items():
            self._publishers[name].publish(roslibpy.Message(msg))

    def read(self) -> SensorData:
        now = time.monotonic()

        for field_name, spec in SENSORS.items():
            last_time = self._last_msg_time[field_name]

            if last_time != 0.0 and now - last_time > spec.timeout:
                setattr(
                    self.sensor_data,
                    field_name,
                    spec.type(),
                )

                setattr(
                    self.sensor_data.raw,
                    field_name,
                    None,
                )

                self._last_msg_time[field_name] = 0.0

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
        for pub in self._publishers.values():
            pub.unadvertise()

        self._publishers.clear()

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
